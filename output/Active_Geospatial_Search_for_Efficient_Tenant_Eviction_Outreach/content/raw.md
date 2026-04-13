# Active Geospatial Search for Effcient Tenant Eviction Outreach

Anindya Sarkar<sup>1</sup> , Alex DiChristofano<sup>3</sup> , Sanmay Das<sup>2</sup> , Patrick J. Fowler<sup>34</sup> , Nathan Jacobs<sup>1</sup> , Yevgeniy Vorobeychik<sup>1</sup>

Department of Computer Science and Engineering, Washington University in St. Louis, USA Department of Computer Science and Engineering, George Mason University Division of Computational & Data Sciences, Washington University in St. Louis, USA Brown School at Washington University in St. Louis, USA

### Abstract

Tenant evictions threaten housing stability and are a major concern for many cities. An open question concerns whether data-driven methods enhance outreach programs that target at-risk tenants to mitigate their risk of eviction. We propose a novel *active geospatial search (AGS)* modeling framework for this problem. AGS integrates property-level information in a search policy that identifes a sequence of rental units to canvas to both determine their eviction risk and provide support if needed. We propose a hierarchical reinforcement learning approach to learn a search policy for AGS that scales to large urban areas containing thousands of parcels, balancing exploration and exploitation and accounting for travel costs and a budget constraint. Crucially, the search policy adapts online to newly discovered information about evictions. Evaluation using eviction data for a large urban area demonstrates that the proposed framework and algorithmic approach are considerably more effective at sequentially identifying eviction cases than baseline methods.

### Introduction

Evictions can have a profound impact on tenants, causing instability in the rental market and exacerbating the already signifcant crisis of affordable housing and homelessness in many large urban areas. While the response to the COVID-19 pandemic in the United States was to impose moratoria on evictions at federal, state, and local levels, these have now been lifted. Moreover, most of the \$46 billion allocated in housing assistance for low-income households through the Emergency Rental Assistance (ERA) program has now been spent. As a result, eviction rates in the US are rising, with an average of 3.6 million eviction cases fled annually (Gromis et al. 2022; Marc¸al, Fowler, and Hovmand 2023). Eviction concerns are especially acute due to the inequitable impact on marginalized communities. Female, Black, and families with children disproportionately experience eviction (Collinson et al. 2022; Graetz et al. 2023). Exposure to unstable and substandard housing can be particularly hard on children, leading to developmental effects that can follow them for the rest of their lives (Desmond, Gershenson, and Kiviat 2015).

While one way to mitigate the risks and consequences of evictions is through policy, a complementary approach canvasses households at risk of eviction to provide resources to help tenants avoid it. For example, providing information about the availability of effective legal representation can be instrumental, as far fewer tenants than landlords have legal representation in eviction proceedings (Desmond 2016). Legal representation for renters has a signifcant impact, reducing the likelihood of eviction warrants and possessory judgments while also imposing smaller monetary judgments (Cassidy and Currie 2023; Greiner, Pattanayak, and Hennessy 2013).In addition, subsidies that help low-income tenants with utility payments (HHS 2023), along with lowincome housing programs such as Section 8 vouchers (HUD 2023), can improve their ability to pay rent and avoid eviction. Proactively providing information about these programs can thus also signifcantly mitigate eviction risk.

Canvassing tenants at risk of eviction, however, is labor intensive. Canvassers working individually or in teams struggle to reach the vast number of low-income housing units behind on rent. It is, consequently, crucial to make effcient use of such limited resources to provide the maximum beneft possible. However, another important challenge is that we do not know, a priori, the risk of eviction for any given household. We can use past data to learn a predictive model for eviction risk, as demonstrated by Mashiat et al. (2024). However, such predictions can rapidly become stale, and data we can use to train is not equally available everywhere. Thus, we need to effectively use a limited canvassing budget to identify at-risk households while improving the quality of predictions we make in identifying such households. This ultimately necessitates effectively trading off exploration, which allows us to improve predictions of households likely to be evicted and exploitation aimed at reaching the most at-risk households.

We introduce a novel *active geospatial search (AGS)* framework to model this problem. In AGS, an agent (e.g., canvasser) has a limited budget C that can be used to query a series of locations (rental units, buildings) embedded in a geographical area. Each query returns a signal whether or not the location has a target property (an impending eviction, high eviction risk, etc), but incurs a cost which may depend on the previous query (for example, representing travel time between two locations). The goal in AGS is to fnd a

Copyright © 2025, Association for the Advancement of Artifcial Intelligence (www.aaai.org). All rights reserved.

search policy to maximize the total number of locations with the target property (henceforth, targets) identifed within the limited search budget. Additionally, some eviction data is available—for example, from past court flings, or evictions in a specifc geographical region—but not directly applicable to the search problem at hand. For example, we may have data for past evictions but need to identify *impending* evictions (effectively, evictions that have yet to occur).

AGS builds conceptually on two closely related models: conventional active search and visual active search. In conventional active search (Garnett et al. 2015; Jiang et al. 2017a; Jiang, Garnett, and Moseley 2019), one sequentially queries labels for a given dataset of inputs, but no prior labeled data or relationship topology that relates inputs to one another in a semantically meaningful way is provided. Thus, typical approaches use myopic and non-myopic heuristics for balancing exploration (to learn a model that predicts labels given inputs) and exploitation coupled with relatively simple predictive models (such as k-nearest neighbors). Visual active search (VAS) (Sarkar et al. 2022; Sarkar, Jacobs, and Vorobeychik 2023) was recently developed to address active search in which queries are associated with small regions within a large-scale overhead image, with labels corresponding to the existence of a target object within the region. However, the VAS model is intimately tied to a visual representation of the search area, and therefore, solutions to this problem cannot be directly applied in the AGS setting.

We propose a hierarchical reinforcement learning (RL) approach for scalable AGS. Our frst step is a key building block: composing prediction and search modules, with the latter trained using RL loss, while the parameters of the prediction module are updated using the supervised loss using labels obtained from queries. The technical challenge is that this approach scales poorly as we consider large geographical areas with thousands of parcels (as our experiments demonstrate). To address this, we propose a hierarchical policy and learning framework, *hierarchical AGS (HAGS)*. In HAGS, the area is divided into regions. We then learn a shared region-level prediction module, a shared region-level search policy that determines the next parcel to query within a relatively small geographical region (as in the frst approach), and the high-level policy, which is trained to select which region to query.

We evaluate the proposed approach using eviction data for a large urban area. First, we show that in settings with uniform query costs and those in which query costs depend on inter-location distance, HAGS outperforms all baselines, including the reinforcement learning approach for smallarea AGS, often by a large margin. Second, we show that structural (tabular) features are slightly more useful in isolation than overhead images of parcels, and the combination provides a tangible improvement, demonstrating the value of multimodal information in this context. In summary, we make the following contributions:

- We propose a novel model of geospatial exploration, *active geospatial search (AGS)*, motivated by the problem of mitigating eviction risk.
- We develop an end-to-end deep reinforcement learning

pipeline to solve AGS in small-area search problems.

- We develop a hierarchical framework to tackle AGS, *HAGS*, in large-area search problems.
- We demonstrate the effcacy of HAGS using eviction data from a large urban area, showing that it outperforms all baselines, including conventional active search and a naive application of RL for small-area AGS.

### Related Work

Our work is part of a larger body of literature focusing on geospatial applications of optimization and artifcial intelligence in nonproft and humanitarian domains. This includes developing solutions for collaborative recycling (Hemmelmayr, Smilowitz, and de la Torre 2017), the sequential redistribution of food donations (Balcik, Iravani, and Smilowitz 2014), the routing of disaster relief (de la Torre, Dolinskaya, and Smilowitz 2012), predicting micronutrient defciency (Bondi-Kelly et al. 2023), and anti-poaching measures (Fang et al. 2016; Fang, Stone, and Tambe 2015; Bondi et al. 2018a, 2020, 2018b; Xu et al. 2020). However, none of these modeling and solution approaches can be directly applied to the AGS framework in mitigating eviction risk through canvassing and information distribution.

Active Search AGS builds on conventional *active search*, frst proposed by Garnett et al.. Previous work in active search has focused on developing nonmyopic algorithms (Jiang et al. 2017b), minimizing the cost to fnd a given number of examples of the target class (Jiang, Garnett, and Moseley 2019).Recently, *visual active search (VAS)* has been proposed as a variation of active search in which the search region is a satellite image (Sarkar et al. 2022; Sarkar, Jacobs, and Vorobeychik 2023). However, VAS is focused on visual data and is not directly applicable to AGS.

Geospatial Applications of Visual Data Geospatial information linked with images has proved useful for the dynamic modeling of traffc (Workman and Jacobs 2020) and the enhancement of near/remote sensing (Workman et al. 2022). The use of imagery as a source of property information is motivated by the work of Lee, Zhang, and Crandall (2015) who use images from Flickr to predict geoinformative attributes of the location being photographed, Gebru et al. (2017) who estimate socioeconomic characteristics of neighborhoods based on Google Street View images, and Archbold et al. (2023) who develop fne-level estimates of property value at the pixel level from overhead images.

Eviction and Tenant Harassment Prediction Work by Ye et al. (2019) and Mashiat et al. (2024) in the housing domain has shown promise in utilizing machine learning to predict tenant harassment, but lacks the utilization of high-dimensional visual information as well as a sequential decision-making policy. On the other hand, Tabar et al. (2022b) have used satellite imagery data to predict whether a given census tract is an eviction hot spot for the county in which it sits, but their model yields a high-level picture of eviction risk, with census tracts covering 4,000 people on average. Other efforts to harness data science methods to predict and understand evictions include forecasting the number of tenants at risk of formal eviction in the next month in a census tract (Tabar et al. 2022a), and understanding the predictors of eviction and future eviction hot spots in San Francisco (Tan 2020).

# Active Geospatial Search for Eviction Prevention

In this work, we consider the problem of discovering properties with tenants at risk of an upcoming eviction fling, with the goal of reducing this risk, for example, by providing information about fnancial and legal resources. We model this as a *active geospatial search (AGS)* problem. At the high level, AGS involves sequential exploration and discovery, with the ultimate goal of identifying as many locations with a pre-specifed target property as possible given limits on time and resources. Formally, a geospatial search task consists of a set of K parcels (e.g., rental buildings) embedded as points in a geographic region. Each parcel i is associated with a feature vector x<sup>i</sup> as well as a geospatial location l<sup>i</sup> ∈ R 2 . Attributes in x<sup>i</sup> can include visual data (such as satellite imagery) as well as tabular data (such as the number of units in the building, year built, and so on). Let x = (x1, . . . , xK) aggregate all of this parcel-level attribute information. Each parcel i is also associated with a binary label y<sup>i</sup> ∈ {0, 1}, where y<sup>i</sup> = 1 iff parcel i has the property of interest (e.g., a likely eviction fling in the near future, for example, over the next three months). Let y = (y1, . . . , yK) denote the vector of labels over all parcels.

A central feature of AGS is that at the beginning of the search, we have label information for a subset of parcels obtained, for example, using a recent history of evictions. For the rest, our task amounts to both learning (exploration) and discovery (exploitation). Specifcally, we generate a sequence of location queries {qt}, where each q<sup>t</sup> queries a label y<sup>i</sup> at location i = qt. Let c(i, j) as the cost associated with querying parcel j when initiating the query process from parcel i. To account for the initial query, we introduce a dummy starting parcel d, where c(d, k) is the initial query cost. Let C be the query budget constraint. The objective of AGS is to identify as many target parcels as we can within the total budget constraint, which we represent as the following optimization problem:

$$
\max_{\{q_t\}} \sum_t y_{q_t} \quad \text{s.t.}: \quad \sum_{t \ge 0} c(q_{t-1}, q_t) \le C \tag{1}
$$

where c(q<sup>−</sup>1, q0) = c(d, q0) is the cost of the frst query.

### Proposed Approach

We begin by considering AGS in a small area; this will provide key building blocks for addressing large-area AGS that we deal with below. Specifcally, we propose an approach for *learning* a search policy from past query results for a subset of locations, which is then deployed to solve Problem (1), balancing exploration (using queries to improve our ability to predict likely target locations) and exploitation (identifying locations that are subject to eviction proceedings, either ongoing or impending). Our frst step to this

![](_page_2_Figure_8.jpeg)

Figure 1: Policy network architecture.

end is to model AGS as a budget-constrained Markov decision process (MDP), akin to Sarkar, Jacobs, and Vorobeychik (2023). In this MDP, the input state at time t includes: 1) aggregated feature vectors of the K parcels, x t , which are crucial in providing a broad perspective on the current search state, 2) the outcomes of past search queries o t , and 3) the remaining budget B<sup>t</sup> ≤ C. We represent outcomes of search query history o as follows. Each element of o corresponds to a parcel index i, so that o <sup>t</sup> = (ot1, . . . , otK), where oti = 0 if i has not been previously queried, and oti = 2(yi) − 1, if parcel i has been previously queried.

In this MDP, the actions are choices over which parcels to query next. In particular, we denote the set of parcels by A = {1, ..., K}. Since, in our model, there is never any value to querying a parcel more than once, we restrict actions available at each step to only parcels that have not yet been queried. We assign an immediate reward for query a parcel i as R(x, i) = y<sup>i</sup> . Finally, state transitions involve updating the remaining budget by subtracting the current query cost and incorporating the result of the most recent search query into the outcomes of past search queries.

We begin by proposing a reinforcement learning (RL) approach for learning a search policy when the set of locations available (that is, K) is small, limiting the number of actions our search needs to consider. However, this approach fails to scale to large geographical regions. Therefore, we subsequently tackle the scalability challenge by proposing an approach for learning *hierarchical* search policies.

### Small-Area Search

Suppose that we consider a relatively small geographical area so that the total number of parcels K, and therefore, the number of actions |A| that we need to consider, is relatively small. We propose a RL approach for solving this problem. Specifcally, we use the REINFORCE algorithm to directly learn a search policy ψθ(x, o, B), where θ are the parameters of the policy that we learn (Williams 1992).

In order to utilize the information we acquire during search, following Sarkar, Jacobs, and Vorobeychik (2023), we propose a search policy comprised of two key components: 1) the prediction module represented by fϕ(x, o) and 2) the search module denoted as g<sup>ζ</sup> (p, o, B), where ϕ and ζ represent trainable parameters and p = fϕ(x, o) is the vector of predicted eviction probabilities with p<sup>i</sup> the predicted probability of at least one eviction in parcel index i. Conceptually, f<sup>ϕ</sup> generates predictions by exclusively considering the task features x and previous search outcomes o, whereas

g<sup>ζ</sup> depends solely on information pertinent to the search process itself, including the predicted eviction probabilities p, previous search outcomes o, and the remaining budget B. The resulting search policy is a combination of these modules, expressed as ψ(x, o, B) = g<sup>ζ</sup> (fϕ(x, o), o, B) (Fig. 1).

Throughout the episode, we keep the search module g<sup>ζ</sup> fxed, using it to generate a sequence of queries, which inherently incorporates an element of exploration due to the stochastic nature of the policy. As we observe labels y<sup>j</sup> for each queried parcel j during the episode, we update the prediction function f<sup>ϕ</sup> using binary cross-entropy loss (LBCE). Once the episode concludes (when we have exhausted the search budget C) we update both the search policy parameters ζ and the initial prediction function parameters ϕ. This update involves a combination of RL and supervised loss. In the case of the search module, we calculate the cumulative sum of rewards R = P i y<sup>i</sup> for the parcels i queried during the episode, and employ the RL loss LRL based on the RE-INFORCE algorithm. For the prediction module, we utilize the collected labels y<sup>i</sup> from the episode and apply LBCE loss. The proposed approach explicitly balances the RL and supervised loss through the loss function:

$$
\mathcal{L}_{AGS} = (\mathcal{L}_{RL} + \lambda \mathcal{L}_{BCE}). \tag{2}
$$

This ensures that the policy is trained *to adapt to the evolving prediction dynamics during the episode*. Here λ is a hyperparameter. A detailed presentation of the complete method is provided in Algorithm 2 in Supplement. During the inference phase, we fx the parameters of the search module ζ, and udpate the parameters of the prediction module ϕ after each query outcome is observed using the LBCE loss.

### Large-Area Search

The key assumption in the approach above is that the number of candidate parcels is relatively small. In practice, that is unrealistic, since even a reasonable target geographical area may contain tens of thousands of parcels. Since the architecture described above requires a policy output per action (parcel), it cannot scale to such problems (see Section ).

To address this issue, we propose a hierarchical search framework, *Hierarchical AGS (HAGS)*. The key insight behind HAGS is that we can leverage shared structure—in particular, symmetry and geospatial locality—of the geospatial domain to introduce inductive bias that signifcantly reduces learning and decision complexity.

Specifcally, let the geospatial area of interest be comprised of N regions, where each region is, in turn, comprised of (at most) K parcels. This induces a hierarchical decomposition of the area frst into regions (frst level), and then (within each region) into parcels (second level). In HAGS, the frst level of decision making will therefore correspond to choosing a region, while the second will entail choosing a parcel within the selected region. Consequently, a level-1 (higher-level) policy will choose among the N regions, whereas a level-2 policy for each region r will, in turn, choose among the K parcels. For a region r, let x<sup>r</sup> = (xr1, . . . , xrK) denote the collection of attributes for each parcel in r, and let x = (x1, . . . , x<sup>N</sup> ) aggregate all of these into a single global feature vector over all regions. Similarly, o<sup>r</sup> is a vector of observed query responses over the parcels in region r, with o combining them into a single global vector.

In HAGS, as in our approach for small-area search above, we decompose the search problem into two pieces: 1) a prediction module fϕ(xr, or) which outputs parcel-level predictions given region-level inputs x<sup>r</sup> and or, and 2) a hierarchy of search policies, as visualized in Figure 2. The main idea in our HAGS architecture is to leverage geospatial structure by a) learning a single prediction module fϕ(xr, or) with parameters ϕ shared across both the frst and second levels of decision making, and b) learning a single level-2 policy g h2 θ (xr, or, B) shared by all regions. This introduces an inductive bias, taking advantage of geospatial structure to signifcantly reduce the number of parameters we need to learn.

Specifcally, let p = fϕ(x, o) denote predictions for *all* regions, aggregated from individual region-level predictions, with pri the predicted probability that parcel i in region r has the target property (e.g., an impending eviction proceedings). Let p¯<sup>r</sup> = P i pri be the predicted expected number of parcels with the target property in region r ( where i ranges over parcels in region r). Let g h1 ζ (¯p, o, B) denote the level-1 policy that outputs a distribution over regions to query next, given inputs p, o (aggregated over all regions) and remaining budget B. Similarly, let g h2 θ (pr, or, B) be a shared level-2 policy (shared across all regions) that given regionspecifc inputs pr, or, along with B outputs a distribution over parcels in the associated region. At training time, actions are sampled from these distributions, whereas at search time we choose the action with the highest probability.

We jointly train the parameters of the prediction module, as well as both the level-1 and level-2 policies, using the RE-INFORCE policy gradient framework, with the loss function

$$
\mathcal{L}_{HAGS} = (\mathcal{L}_{RL}^{h1} + \mathcal{L}_{RL}^{h2} + \lambda \mathcal{L}_{BCE}), \tag{3}
$$

where L h1 RL and L h2 RL are the standard REINFORCE loss functions for level-1 and level-2 policies, respectively, and LBCE the supervised binary cross-entropy loss used to train the prediction module. The RL rewards for the level-2 policies are just as in AGS, that is, 1 if the queried parcel has the target property and 0 otherwise. For level-1 policies, the reward associated with a chosen parcel is 1 if the query according to the level-2 policy within this region yields the target property, and 0 otherwise. Note that LBCE plays an identical role as it did in small-area search AGS framework, that is, we dynamically modify the parameters of the prediction module (ϕ) following the observation of each query outcome both during training and inference. This adjustment is achieved through the utilization of the LBCE loss, which computes the binary cross-entropy loss between the predicted label and the observed label y for the queried parcel. During gradient descent steps, we backpropagate L h1 RL and LBCE through the prediction module and backpropagate L h2 RL through the level-2 policy, updating parameters of both f and the associated search policy. A detailed formal presentation of the method is provided in Algorithm 1.

![](_page_4_Figure_0.jpeg)

Figure 2: HAGS policy network architecture.

| Search Budget        | 15    | 20    | 25    | 50    | 75    | 100   | 200   | 300   | 400   |
|----------------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Random               | 1.00  | 1.75  | 2.00  | 2.25  | 2.50  | 2.75  | 9.75  | 12.50 | 21.75 |
| Conventional AS      | 2.25  | 3.25  | 4.50  | 5.75  | 6.50  | 7.50  | 15.75 | 22.00 | 32.50 |
| Greedy by Unit Count | 5.25  | 5.50  | 7.00  | 12.50 | 20.00 | 25.75 | 36.25 | 46.00 | 55.25 |
| Greedy               | 7.50  | 9.25  | 10.50 | 17.75 | 21.00 | 29.50 | 44.50 | 59.00 | 65.75 |
| Greedy Adaptive      | 8.75  | 10.75 | 14.00 | 22.25 | 27.50 | 34.75 | 54.50 | 65.50 | 72.25 |
| AGS                  | 8.00  | 10.25 | 11.50 | 18.75 | 22.00 | 31.50 | 46.25 | 61.25 | 68.25 |
| HAGS                 | 10.25 | 12.75 | 14.50 | 25.75 | 29.50 | 38.50 | 57.75 | 70.50 | 77.75 |

![](_page_4_Table_2.jpeg)

Table 1: ANT as a function of search budget for uniform query cost; average eviction rate is 5%.

| Search Budget        | 15    | 20    | 25    | 50    | 75    | 100   | 200   | 300    | 400    |
|----------------------|-------|-------|-------|-------|-------|-------|-------|--------|--------|
| Random               | 1.25  | 2.25  | 2.75  | 5.50  | 7.75  | 9.50  | 16.25 | 29.75  | 46.75  |
| Conventional AS      | 3.50  | 5.50  | 6.75  | 11.25 | 15.50 | 18.00 | 27.50 | 43.50  | 65.50  |
| Greedy by Unit Count | 8.00  | 11.25 | 14.25 | 23.25 | 32.25 | 42.25 | 50.00 | 72.00  | 105.50 |
| Greedy               | 9.75  | 12.75 | 17.00 | 28.75 | 38.25 | 51.00 | 74.25 | 103.50 | 119.75 |
| Greedy Adaptive      | 10.50 | 14.50 | 18.75 | 34.50 | 49.25 | 57.50 | 86.75 | 117.75 | 144.50 |
| AGS                  | 10.50 | 14.00 | 17.25 | 29.25 | 41.50 | 53.25 | 79.25 | 106.75 | 128.25 |
| HAGS                 | 13.25 | 18.00 | 22.25 | 38.50 | 51.75 | 60.00 | 91.75 | 124.50 | 151.75 |

![](_page_4_Table_4.jpeg)

Table 2: ANT as a function of search budget for uniform query cost; average eviction rate is 10%.

## Experiments

We evaluate the effcacy of the AGS framework and the proposed HAGS approach using observed eviction flings in a mid-sized region. Our *evaluation metric* is the average number of targets (ANT) found within a given budget (averaged over search runs). We consider two query cost settings: (i) uniform query costs, i.e., c(i, j) = 1 for all parcels i, j, and (ii) distance-based cost, where c(i, j) is proportional to the distance between i and j. Next, we describe in detail the data we use, as well as the baseline methods, before presenting our results. Our focus here is on large-area search; we defer most results involving small-area search to the Supplement.

Data We construct features associated with parcels from two sources: tabular data and overhead (satellite) images. The tabular features are based on those in Mashiat et al. (2024), and encompass eviction court flings, owner information, property-level attributes, and neighborhood features. These data are originally derived from a collection of municipal sources across St. Louis City and County, excluding neighborhood features, which are obtained from the American Community Survey (ACS) (acs 2021). Court eviction flings are aggregated over the previous year, as well as semiannually, quarterly, and monthly. Property information includes the number of housing units and whether it is owner-occupied. Properties are linked to owners, and information on linked owners is included, such as the number of properties owned, in- versus out-of-state residence, and whether the owner has worked with a moderate- or high-fling attorney (defned as a fling rate above one and three standard deviations above the mean for attorneys during that period, respectively). Neighborhood features are at the Census block-group level, and describe areas of 600- 3000 households in terms of average rent as a percentage of household income, the median household income, the ratio of income to the poverty level, racial and ethnic composition, the number of total housing units, the proportion of occupied and vacant units, and the proportion of owner and renter-occupied units. We restrict our analysis to residential,

### Algorithm 1: The proposed HAGS algorithm for training.

- Require: A search task (x = [x1, . . . , x<sup>N</sup> ]; y = [y1, . . . , y<sup>N</sup> ]), where x<sup>r</sup> = [xr1, . . . , xrK] and y<sup>r</sup> = [yr1, . . . , yrK] ; budget C; Hierarchy 1 policy: g h1 ζ (p = fϕ(x, o), B) with parameters ζ; Hierarchy 2 policy: g h2 θ (pr, or, B) with parameters θ; o = [o1, . . . , o<sup>N</sup> ] with o<sup>r</sup> = [or1, . . . , orK];
- 1: Initialize o<sup>r</sup> = [0...0] for r ∈ {1, . . . , N}; B <sup>t</sup> = C; t = 0
- 2: while B <sup>t</sup> > 0 do
- 3: p = fϕ(x, o); here p = [p1, . . . , p<sup>N</sup> ] with p<sup>r</sup> = [pr1, . . . , prK]
- 4: *j* ←− Samplej∈{1,...r,...,<sup>N</sup> }Softmax [¯p]; here p¯ = [¯p1, . . . , p¯<sup>N</sup> ] and p¯<sup>r</sup> = P i pri with i ∈ {1, . . . , K}.
- 5: Explore region with index j at time t.
- 6: s˜ = g h2 θ (p<sup>j</sup> , o<sup>j</sup> , B<sup>t</sup> ) ; *r* ←− Sampler∈{1,...i,...,K} [˜s]
- 7: Query parcel r within region j and observe true label yjr. 8: Update ϕ t to ϕ <sup>t</sup>+1 using LBCE loss between p and pseudo label yˆ t , each component of yˆ t is defned as
- 9: yˆ t jr ←− yjr if r'th parcel within region j has been queried pjr if yjr is Unobserved.
- 10: Set R <sup>t</sup> = yjr, Update o t to o <sup>t</sup>+1 with ojr = 2yjr − 1, update B <sup>t</sup>+1 = B <sup>t</sup> − c(k, j), k is the parcel queried at t − 1.
- 11: Collect transition tuple, τ t = state = (x, o<sup>t</sup> , B<sup>t</sup> ), level 1 policy action = j, level 2 policy action = r, reward of both policies = R t , next state of level 1 policy = (x, o<sup>t</sup>+1, B<sup>t</sup>+1), next state of level 2 policy = (pz, o<sup>t</sup>+1 <sup>z</sup> , , B<sup>t</sup>+1) assuming level 1 policy selects region z at (t+1).
- 12: *t* ←− t + 1
- 13: end while
- 14: Update hierarchy 1 policy parameters using (L h1 RL) based on (τ t ) collected throughout the episode and also update ϕ using (LBCE ) based on the collected labels (yjr) over the episode.
- 15: Update hierarchy 2 policy parameters θ using (L h2 RL) based on the collected transition tuples (τ t ) throughout the episode.
- 16: Return Updated hierarchy 1 and 2 policy parameters.

non-vacant parcels with at least two rental units, yielding a total of 26700 properties across St. Louis City and County. The time period used for training all AGS and baseline approaches is July 1, 2021, to September 30, 2022. Testing covers the period between October 1, 2022, and December 31, 2022, where the target is positive if an eviction fling occurred at the property during that period.

Satellite imagery data comes from the National Agriculture Imagery Program (NAIP) (NAIP 2023). Images were captured during June 2022 at a resolution of 60 centimeters. We extracted 214×214 patches such that these patches fully covered 95% of the properties. Since we possess visual data for each individual parcel as well as tabular features containing past eviction records for the corresponding parcels, we utilize methods from multi-modal representation learning (Ngiam et al. 2011; Tsai et al. 2019). This enables us to seamlessly amalgamate information from both modalities, culminating in a latent representation for each parcel. We leverage a multi-modal architecture as in (Tsai et al. 2019). We depict the Multi-Modal Feature Extraction (MMFE) module in the Appendix in Fig. ??. The parameters of MMFE modules are shared across the parcels.

Baseline Methods We compare the proposed approach to the following baselines:

- 1. *Random:* Each parcel is chosen uniformly randomly among those not yet explored.
- 2. *Greedy:* we train a classifer fgreedy to predict whether a particular property will have at least one eviction fling within the next three months and search the most likely properties until the search budget is exhausted.
- 3. *Greedy by unit count:* query the parcel with the largest number of units.
- 4. *Greedy adaptive:* similar to *Greedy* except the prediction model f is updated at each step based on query outcomes.
- 5. *Conventional active search*, an active search method by Jiang et al. (2017a), using a low-dimensional feature representation for each parcel from the same MMFE feature extraction network as in our approach.

In addition, we use the simple small-area AGS approach as a baseline in the large-area search setting (involving 16000 parcels; see below for further details).

### Results

Starting with the original 26700 parcels, we randomly select 16000 properties for evaluation, averaging the results over four such random selections to compute ANT. The selected properties are bootstrapped to have a particular average number of positive targets (that is, properties with eviction flings during the prediction period) to enable us to study the impact of target sparsity. We consider mean positive rates of 5% and 10%, with s.t.d. of 0.01%, and 0.02%, respectively. In HAGS, we divide the entire search space into N = 160 regions, each containing K = 100 parcels.

Uniform-Cost Search We frst consider uniform-cost settings. In this case, we consider search budgets C of 15, 20, 25, 50, 75, 100, 200, 300, and 400 queries. The results are presented in Tables 1 and 2 for positive rates of 5% and 10%, respectively. In all cases, HAGS outperforms all baselines, often by a large margin. In particular, improvement ranges from 3%-17% over the most competitive baseline. Particularly noteworthy is the poor performance of "fat" AGS designed for small-area search. While AGS outperforms most baselines, it nevertheless exhibits poor effcacy compared to HAGS and, indeed, is slightly worse than the simple greedy adaptive search heuristic. This suggests the inductive bias introduced in the hierarchical architecture of HAGS is crucial to obtaining high effcacy at scale. We also observe a general pattern of greatest improvement from HAGS in settings with lower budgets (greatest improvement is for C = 15), although neither pattern is monotonic. Additionally, a lower overall target (eviction) rate has a greater average improvement (average improvement for 5% target rate is ∼7%, compared to ∼5% for 10% target rate), although this pattern is not uniform across budgets. The general pattern is that the signifcance of effcient balancing between exploration and exploitation as exhibited by HAGS is most notable when there is scarcity in either budget or availability of targets to discover.

Distance-Based Search Costs Next, we consider HAGS compared to baselines in the case when search costs are not uniform, but instead are based on relative distances between parcels. Specifcally, we determine the po-

| Search Budget        | 300  | 600  | 1200 | 2400 | 4800 | 10000 | 20000 | 40000 | 80000 |
|----------------------|------|------|------|------|------|-------|-------|-------|-------|
| Random               | 0.00 | 0.25 | 0.25 | 0.50 | 0.50 | 0.75  | 0.75  | 1.00  | 2.25  |
| Conventional AS      | 0.00 | 0.00 | 0.25 | 0.75 | 1.00 | 1.00  | 1.25  | 1.50  | 2.00  |
| Greedy by Unit Count | 0.00 | 0.00 | 0.00 | 1.00 | 1.25 | 1.25  | 1.75  | 2.00  | 2.75  |
| Greedy               | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00  | 1.00  | 1.75  | 2.75  |
| Greedy Adaptive      | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00  | 1.00  | 1.75  | 2.75  |
| AGS                  | 1.25 | 1.50 | 1.50 | 1.50 | 1.50 | 1.75  | 1.75  | 2.00  | 2.50  |
| HAGS                 | 2.00 | 2.50 | 2.50 | 2.50 | 2.75 | 2.75  | 2.75  | 3.50  | 4.50  |

![](_page_6_Table_0.jpeg)

Table 3: ANT as a function of budget for distance-based query cost; average eviction rate is 5%.

| Search Budget        | 300  | 600  | 1200 | 2400 | 4800 | 10000 | 20000 | 40000 | 80000 |
|----------------------|------|------|------|------|------|-------|-------|-------|-------|
| Random               | 0.00 | 1.00 | 1.00 | 1.25 | 1.25 | 1.25  | 1.50  | 1.75  | 2.25  |
| Conventional AS      | 0.00 | 0.00 | 0.50 | 1.00 | 1.75 | 1.75  | 2.00  | 2.00  | 2.75  |
| Greedy by Unit Count | 1.00 | 1.00 | 1.00 | 1.00 | 1.50 | 1.75  | 2.25  | 2.75  | 3.75  |
| Greedy               | 1.25 | 1.25 | 1.50 | 1.50 | 1.50 | 2.00  | 2.50  | 3.00  | 3.75  |
| Greedy Adaptive      | 1.25 | 1.25 | 1.50 | 1.50 | 1.50 | 2.00  | 2.50  | 3.00  | 3.75  |
| AGS                  | 1.50 | 1.75 | 1.75 | 1.75 | 1.75 | 2.00  | 3.00  | 3.50  | 4.25  |
| HAGS                 | 2.25 | 2.50 | 2.75 | 2.75 | 3.00 | 3.25  | 4.00  | 5.75  | 6.25  |

![](_page_6_Table_2.jpeg)

Table 4: ANT as a function of budget for distance-based query cost; average eviction rate is 10%.

|                           | Average Positive Rate of 2.5% |                         |                         | Average Positive Rate of 5% |                         |                         | Average Positive Rate of 10% |                         |                         |
|---------------------------|-------------------------------|-------------------------|-------------------------|-----------------------------|-------------------------|-------------------------|------------------------------|-------------------------|-------------------------|
| Search Budget             | 15                            | 20                      | 25                      | 15                          | 20                      | 25                      | 15                           | 20                      | 25                      |
| AGS-VIS<br>AGS-TAB<br>AGS | 0.932<br>1.008<br>1.052       | 1.092<br>1.184<br>1.288 | 1.268<br>1.340<br>1.352 | 1.840<br>1.972<br>2.240     | 2.216<br>2.336<br>2.596 | 2.532<br>2.640<br>2.828 | 3.496<br>4.216<br>4.372      | 4.100<br>5.004<br>5.204 | 5.044<br>5.501<br>5.632 |

![](_page_6_Table_4.jpeg)

Table 5: Ablation Study Average Number of Targets (ANT) Found by Search Task Parameters and Solution Method

sition of each parcel using GPS coordinates and calculate the query cost as the Manhattan distance in meters between parcel locations. We vary search budgets C ∈ {300, 600, 1.2k, 2.4k, 4.8k, 10k, 20k, 40k, 80k}, and again consider 5% and 10% positive rate in the area. The results are presented in Tables 3 and 4. In this setting, we see an even greater improvement of HAGS over the baselines (including, again, AGS), with improvement over the most competitive baseline ranging from approximately 42% to 70%. Notably, when the average positive rate is low (5%), the greedy (exploitation-only) baselines have trouble fnding *any* targets within the available budget.

Ablation Study of Visual and Structured Data Finally, we address an important qualitative question in the particular context of tenant eviction data analytics: to what extent is visual and structured (tabular) data contribute to decision effcacy? We study this in a small-area search setting, where we randomly select a region containing 100 parcels. In particular, we train AGS (no need for HAGS here) using visual-only data (*AGS-VIS*), tabular-only data (*AGS-TAB*), and both (standard *AGS*). We also provide results of random queries for calibration purposes. The results are provided in Table 5. First, note that both *AGS-VIS* and *AGS-TAB* outperform random search by a large margin. Second, the results suggest that while tabular features tend to be more informative than visual features individually in this setting, integrating visual and tabular features through multi-modal representation learning meaningfully (albeit not dramatically) enhances search performance across various search tasks in different settings. These results demonstrate the importance of leveraging the multi-modal representation that combines tabular and imagery-based features.

### Conclusion

We introduce the novel AGS framework to identify properties with renters who are at risk of imminent eviction. Through extensive experiments, we demonstrate that our approach increases the number of at-risk properties discovered as compared to several strong baselines by at least 5% and, in some settings, over 50%. This is achieved through a pretraining phase combined with an exploration phase that allows for test-time adaptation. These methods have the potential to dramatically increase both the effectiveness and timeliness of door-to-door outreach by social service agencies, thereby increasing the number of tenants who are connected with legal aid, landlord mediation, one-time fnancial assistance, time-limited case management, or moving assistance.
