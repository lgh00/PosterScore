import os
import sys
import re
import json
import argparse
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, Tuple
# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from marker.converters.pdf import PdfConverter
from marker.renderers.markdown import MarkdownRenderer
from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.schema import BlockTypes
from jinja2 import Template

from utils.model_config import get_model_config

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

def extract_txt_figure(paper_path: str, output_dir: Path):
    """
    Extract text and figure from the paper pdf file.
    """
    # extract raw text and assets
    raw_text, raw_result = extract_raw_text(paper_path, output_dir / "content")

    figures, tables = extract_assets(raw_result, output_dir / "assets")
    return 0

def extract_raw_text(pdf_path: str, content_dir: Path) -> Tuple[str, Any]:
    #log_agent_info(self.name, "converting pdf to raw text")
    config = {
        "recognition_batch_size": 4,
        "layout_batch_size": 4,
        "detection_batch_size": 4, 
        "table_rec_batch_size": 4,
        "ocr_error_batch_size": 4,
        "equation_batch_size": 4,
        "disable_tqdm": False,
    }
    converter = PdfConverter(artifact_dict=create_model_dict(), config=config)
    document = converter.build_document(pdf_path)
    
    # create renderer and get rendered output from the existing document
    renderer = converter.resolve_dependencies(MarkdownRenderer)
    rendered = renderer(document)
    
    text, _, images = text_from_rendered(rendered)
    clean_pattern = re.compile(r"<!--[\s\S]*?-->")
    text = clean_pattern.sub("", text)
    text = preprocess_paper_markdown(text)
    
    content_dir.mkdir(parents=True, exist_ok=True)
    (content_dir / "raw.md").write_text(text, encoding="utf-8")
    
    #log_agent_info(self.name, f"extracted {len(text)} chars")
    
    raw_result = (document, rendered, images)
    return text, raw_result

def extract_assets(result, assets_dir: Path) -> Tuple[Dict, Dict]:
    #log_agent_info(self.name, "extracting assets")
    assets_dir.mkdir(parents=True, exist_ok=True)
    document, rendered, marker_images = result
    
    caption_map = extract_captions(document)
    
    figures = {}
    tables = {}
    image_count = 0
    table_count = 0
    
    for img_name, pil_image in marker_images.items():
        caption_info = caption_map.get(img_name, {'captions': [], 'block_type': 'Unknown'})
        
        if 'table' in img_name.lower() or 'Table' in img_name or caption_info.get('block_type') == 'Table':
            table_count += 1
            path = assets_dir / f"table-{table_count}.png"
            pil_image.save(path, "PNG")
            
            tables[str(table_count)] = {
                'caption': caption_info['captions'][0] if caption_info['captions'] else f"Table {table_count}",
                'path': str(path),
                'width': pil_image.width,
                'height': pil_image.height,
                'aspect': pil_image.width / pil_image.height if pil_image.height > 0 else 1,
            }
        else:
            image_count += 1
            path = assets_dir / f"figure-{image_count}.png"
            pil_image.save(path, "PNG")
            
            figures[str(image_count)] = {
                'caption': caption_info['captions'][0] if caption_info['captions'] else f"Figure {image_count}",
                'path': str(path),
                'width': pil_image.width,
                'height': pil_image.height,
                'aspect': pil_image.width / pil_image.height if pil_image.height > 0 else 1,
            }
    
    with open(assets_dir / "figures.json", 'w', encoding='utf-8') as f:
        json.dump(figures, f, indent=2)
    with open(assets_dir / "tables.json", 'w', encoding='utf-8') as f:
        json.dump(tables, f, indent=2)
    with open(assets_dir / "fig_tab_caption_mapping.json", 'w', encoding='utf-8') as f:
        json.dump(caption_map, f, indent=2, ensure_ascii=False)
    
    return figures, tables

def extract_captions(document):
    caption_map = {}
    
    for page in document.pages:
        for block_id in page.structure:
            block = page.get_block(block_id)
            
            if block.block_type in [BlockTypes.FigureGroup, BlockTypes.TableGroup, BlockTypes.PictureGroup]:
                child_blocks = block.structure_blocks(page)
                figure_or_table = None
                captions = []
                
                for child in child_blocks:
                    child_block = page.get_block(child)
                    if child_block.block_type in [BlockTypes.Figure, BlockTypes.Table, BlockTypes.Picture]:
                        figure_or_table = child_block
                    elif child_block.block_type in [BlockTypes.Caption, BlockTypes.Footnote]:
                        captions.append(child_block.raw_text(document))
                
                if figure_or_table:
                    image_filename = f"{figure_or_table.id.to_path()}.jpeg"
                    caption_map[image_filename] = {
                        'block_id': str(figure_or_table.id),
                        'block_type': str(figure_or_table.block_type),
                        'captions': captions,
                        'page': page.page_id
                    }
            
            elif block.block_type in [BlockTypes.Figure, BlockTypes.Table, BlockTypes.Picture]:
                image_filename = f"{block.id.to_path()}.jpeg"
                if image_filename not in caption_map:
                    nearby_captions = self._find_nearby_captions(page, block, document)
                    caption_map[image_filename] = {
                        'block_id': str(block.id),
                        'block_type': str(block.block_type),
                        'captions': nearby_captions,
                        'page': page.page_id
                    }
    
    return caption_map

def preprocess_paper_markdown(text: str):
        """
        处理论文Markdown文本：删除References和Acknowledgements章节
        :param text: 输入的原始Markdown文件路径
        :return: 输出的处理后文本
        """
        # 定义需要删除的章节标题（小写，用于匹配）
        DELETE_SECTIONS = {"references", "acknowledgements"}
        # 跳过标记：True=当前行需要删除，False=保留
        skip_mode = False
        lines = text.split("\n")
        processed_lines = []

        for line in lines:
            # 去除首尾空白字符（适配行首/行尾多余空格）
            stripped_line = line.strip().lower()

            # ============== 情况1：当前未开启跳过模式 ==============
            if not skip_mode:
                # 判断是否为 Markdown 二级标题（## 开头）
                if stripped_line.startswith("### "):
                    # 提取标题文本（去掉 ## 和空格）
                    section_title = stripped_line[4:].strip()
                    # 匹配到需要删除的章节
                    if section_title in DELETE_SECTIONS:
                        skip_mode = True  # 开启跳过模式
                        continue  # 不保留当前标题行

                # 未触发删除，直接保留该行
                processed_lines.append(line)
            # ============== 情况2：当前已开启跳过模式 ==============
            else:
                # 遇到下一个三级标题，先检查是否进入另一个跳过章节，如果是，不用管，如果不是，关闭跳过模式，保留该行
                if stripped_line.startswith("### "):
                    section_title = stripped_line[4:].strip()
                    # 匹配到需要删除的章节
                    if section_title in DELETE_SECTIONS:
                        continue
                    else:
                        skip_mode = False
                        processed_lines.append(line)
                #进入别的章节，关闭跳过模式
                elif stripped_line.startswith("##"):
                    skip_mode = False
                    processed_lines.append(line)
                # 否则：跳过该行（不保留）
                else:
                    continue
        return "\n".join(processed_lines)

def main():
    parser = argparse.ArgumentParser(description = "PosterScore: A tool to score posters")
    parser.add_argument("--paper_path", type=str, required=True, help="Path to the paper pdf file")
    parser.add_argument("--poster_path", type=str, required=True, help = "Path to the poster's image file")
    parser.add_argument("--model", type=str, default="doubao-seed-2-0-lite-260215", choices=["doubao-seed-2-0-lite-260215", "gpt-4o-2024-08-06", "gpt-4.1-2025-04-14", "gpt-4.1-mini-2025-04-14", "claude-sonnet-4-20250514", "claude-opus-4.5", "gemini-2.5-pro", "glm-4.6v", "glm-4.5v", "glm-4v", "moonshot-v1-8k-vision-preview", "MiniMax-M2", "qwen3-vl-plus"], help="model to score the poster")
    args = parser.parse_args()
    # check .env file
    if not env_path.exists():
        raise ValueError(f"Please create .env file in {env_path}")
    # check paper path
    if not Path(args.paper_path).exists():
        raise ValueError(f"Please set paper path {args.paper_path}")
    poster_name = Path(args.paper_path).parent.name or "test_poster"
    # check poster path
    if not Path(args.poster_path).exists():
        raise ValueError(f"Please set poster path {args.poster_path}")

    # check api key
    required_keys = {"ark": "ARK_API_KEY", "openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "google": "GOOGLE_API_KEY", "zhipu": "ZHIPU_API_KEY", "moonshot": "MOONSHOT_API_KEY", "Minimax": "MINIMAX_API_KEY", "Alibaba": "ALIBABA_API_KEY"}
    model_providers = {"doubao-seed-2-0-lite-260215": "ark","claude-sonnet-4-20250514": "anthropic", "claude-opus-4.5": "anthropic", "claude-opus-4-5-20251101": "anthropic", "gemini": "google", "gemini-2.5-pro": "google", "gpt-4o-2024-08-06": "openai", "gpt-4.1-2025-04-14": "openai", "gpt-4.1-mini-2025-04-14": "openai","glm-4.6": "zhipu", "glm-4.6v": "zhipu", "glm-4.5": "zhipu", "glm-4.5-air": "zhipu", "glm-4.5v": "zhipu", "glm-4": "zhipu", "glm-4v": "zhipu","kimi-k2-turbo-preview": "moonshot", "moonshot-v1-8k-vision-preview": "moonshot","qwen3-max": "Alibaba", "qwen3-vl-plus": "Alibaba","MiniMax-M2":"Minimax"}

    need_key = required_keys[model_providers[args.model]]
    if not os.getenv(need_key):
        raise ValueError(f"Please set {need_key}")
    
    # set output directory
    output_dir = Path(args.paper_path).parent.parent / "output" / poster_name
    output_dir.mkdir(parents=True, exist_ok=True)

    extract_txt_figure(args.paper_path, output_dir)


if __name__ == "__main__":
    main()