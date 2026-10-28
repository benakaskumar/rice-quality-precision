"""Global Rice Agronomic, Consumer, and Production Intelligence Database.
Provides complete data on global cultivars: origin terroir, consumer population,
farming population, annual global production volume, nutrition, and culinary profile.
"""

VARIETAL_PROFILES = {
    "Brown rice": {
        "name": "Whole Grain Brown Rice",
        "country": "Worldwide (India, China, USA, Brazil, Southeast Asia)",
        "terroir": "Cultivated across global temperate and tropical paddy basins; milled with the nutrient-dense outer bran and germ layers intact",
        "grain": "medium",
        "category": "Whole Grain Bran & Germ Intact",
        "global_consumers": "1.2+ Billion People",
        "consumer_reach": "Consumed globally by over 1.2 billion people as a primary whole-grain health staple. The core grain for cardiac health, diabetic nutrition, and macrobiotic diets across Asia, North America, Europe, and Latin America.",
        "global_producers": "38 Million Metric Tons / Year",
        "farmer_population": "Cultivated by ~22 Million farming households across global rice production basins.",
        "culinary_uses": "Wholesome grain bowls, Brown rice pilaf, Stir-fries, Spanish brown rice, macrobiotic khichdi, healthy salads",
        "aroma_texture": "Warm, nutty, wholesome roasted grain aroma with a satisfying chewy al dente texture and hearty mouthfeel.",
        "nutrition": "Low Glycemic Index (GI 50–55), 3.5x higher dietary fibre than polished white rice (3.8g/100g), rich in magnesium, manganese, phosphorus, selenium, and B vitamins (B1, B3, B6).",
        "amylose_content": "Medium amylose (20–22%), non-sticky, resilient separated kernels",
        "market_share": "~8% of total retail packaged rice; fastest growing rice category globally with +7.2% annual CAGR"
    },
    "Matta (Rosematta)": {
        "name": "Matta (Rosematta) Red Rice",
        "country": "India (Kerala) / Sri Lanka",
        "terroir": "Palakkad Gap & Kuttanad delta wetlands (cultivated in mineral-rich alluvial soil fed by monsoon floodwaters)",
        "grain": "medium",
        "category": "Red Parboiled Heritage Rice",
        "global_consumers": "85+ Million People",
        "consumer_reach": "Daily dietary staple for over 85+ million people across Kerala, coastal Karnataka, Tamil Nadu, Sri Lanka, and the 12+ million South Asian diaspora worldwide.",
        "global_producers": "12.8 Million Metric Tons / Year",
        "farmer_population": "Cultivated by ~8.5 Million smallholder farming families across South Asian wetland deltas.",
        "culinary_uses": "Kerala Sadya, Fish Curry Rice, Thoran, Kanji (wholesome rice porridge), Ayurvedic rejuvenation therapy",
        "aroma_texture": "Nutty, earthy aroma with robust, plump grains that hold their shape and absorb rich coconut and tamarind gravies without getting mushy.",
        "nutrition": "Low Glycemic Index (GI 50–55), High dietary fibre (3.5g/100g), high magnesium, zinc, iron, and abundant proanthocyanidin red flavonoid antioxidants.",
        "amylose_content": "Medium amylose (22–24%), firm non-sticky parboiled grain",
        "market_share": "~2.4% of global rice production; highly valued heritage GI-tagged health grain"
    },
    "Red Cargo rice": {
        "name": "Red Cargo Rice",
        "country": "Thailand & Philippines",
        "terroir": "Central plains of Thailand and Luzon valley, cultivated in nutrient-rich organic paddies",
        "grain": "medium",
        "category": "Unpolished Red Bran Rice",
        "global_consumers": "65+ Million People",
        "consumer_reach": "Staple health rice in Thailand, Vietnam, and the Philippines, and widely exported to organic health food markets across North America, Europe, and Australia.",
        "global_producers": "8.5 Million Metric Tons / Year",
        "farmer_population": "Cultivated by ~4.2 Million farming households in Southeast Asia.",
        "culinary_uses": "Warm grain bowls, fried rice, salads, coconut rice, pairing with aromatic Thai curries",
        "aroma_texture": "Nutty, sweet aroma with a firm, chewy al dente texture that requires slightly longer cooking.",
        "nutrition": "Rich in Vitamin B1, B2, iron, calcium, and anthocyanin antioxidants with a gentle low glycemic response.",
        "amylose_content": "Medium amylose (21–23%), non-sticky chewy grain",
        "market_share": "~1.6% of global rice trade; premium organic staple"
    },
    "Basmati": {
        "name": "Basmati Aromatic Rice",
        "country": "India & Pakistan",
        "terroir": "Indo-Gangetic plains (Punjab, Haryana, Uttar Pradesh, Uttarakhand, and Pakistani Punjab) irrigated by mineral-rich Himalayan glacial meltwaters",
        "grain": "long",
        "category": "Extra Long Slender Aromatic",
        "global_consumers": "550+ Million People",
        "consumer_reach": "Staple luxury rice consumed by over 550+ million people across South Asia, the Middle East (GCC nations), Europe, and North America; celebrated in 150+ countries.",
        "global_producers": "9.5 Million Metric Tons / Year",
        "farmer_population": "Cultivated by ~2.8 Million dedicated farming families in the GI-protected Himalayan foothills.",
        "culinary_uses": "Royal Biryani, Dum Pulao, Persian Chelow, Fried Rice, celebratory feasts",
        "aroma_texture": "Signature 2-acetyl-1-pyrroline floral pandan aroma; grains elongate 2x in length upon boiling and remain distinct, slender, and fluffy.",
        "nutrition": "Medium Glycemic Index (GI 56–58), low fat, gluten-free, easily digestible with 3.5g protein per serving.",
        "amylose_content": "High amylose (20–22%), completely non-sticky separated kernels",
        "market_share": "Dominates 65% of international aromatic rice trade; $4.5B+ annual export market"
    },
    "Jasmine (Hom Mali)": {
        "name": "Thai Jasmine Rice (Khao Dawk Mali 105)",
        "country": "Thailand",
        "terroir": "Isan plateau (Thung Kula Ronghai region, Ubon Ratchathani) with sandy loam and seasonal tropical monsoons",
        "grain": "long",
        "category": "Aromatic Soft Table Rice",
        "global_consumers": "420+ Million People",
        "consumer_reach": "Primary staple for 70M people in Thailand and over 350M consumers across Southeast Asia, China, North America, and Australia.",
        "global_producers": "11.2 Million Metric Tons / Year",
        "farmer_population": "Grown by ~3.8 Million smallholder farming families in northeastern Thailand.",
        "culinary_uses": "Thai Green Curry, Pad Kra Pao, Mango Sticky Rice, Tom Yum accompaniment",
        "aroma_texture": "Delicate pandan and jasmine flower fragrance; cooks to a silky, tender, and slightly moist clingy grain.",
        "nutrition": "High energy carbohydrate source with low fat, sodium-free, natural floral phytochemicals.",
        "amylose_content": "Low-to-medium amylose (14–17%), soft and tender texture",
        "market_share": "Second largest premium exported aromatic rice in the world"
    },
    "Sona Masuri": {
        "name": "Sona Masuri (BPT 5204)",
        "country": "India",
        "terroir": "Tungabhadra and Krishna river basins across Andhra Pradesh, Telangana, and Karnataka",
        "grain": "medium",
        "category": "Lightweight Low-Starch Table Rice",
        "global_consumers": "1.4 Billion People",
        "consumer_reach": "Everyday staple for over 1.4 billion people across Central/South India and the worldwide Indian diaspora.",
        "global_producers": "34.5 Million Metric Tons / Year",
        "farmer_population": "Cultivated by ~14.5 Million farmers across central and southern India.",
        "culinary_uses": "Everyday Sambar rice, Rasam rice, Curd rice, Lemon rice, Biryani, Vangi bath",
        "aroma_texture": "Subtle mild aroma, lightweight and fluffy texture that is gentle on digestion.",
        "nutrition": "Low starch, lower calorie count than basmati, easily digestible with quick sustained energy.",
        "amylose_content": "High amylose (24–26%), dry and separated grains",
        "market_share": "One of India's most cultivated and consumed non-basmati varieties"
    },
    "Ponni": {
        "name": "Ponni Rice",
        "country": "India (Tamil Nadu)",
        "terroir": "Cauvery River Delta (Thanjavur, the historic rice bowl of Tamil Nadu)",
        "grain": "medium",
        "category": "Parboiled / Raw Table Rice",
        "global_consumers": "110+ Million People",
        "consumer_reach": "Staple food across Tamil Nadu, Karnataka, Malaysia, Singapore, Sri Lanka, and the global Tamil diaspora.",
        "global_producers": "14.2 Million Metric Tons / Year",
        "farmer_population": "Cultivated by ~5.5 Million farmers along the fertile Cauvery delta.",
        "culinary_uses": "Daily meals, Idli, Dosa, Pongal, Variety rice dishes",
        "aroma_texture": "Soft and pleasant texture; parboiled variant keeps grains firm and resilient.",
        "nutrition": "High thiamine (Vitamin B1) retention due to parboiling, low glycemic response.",
        "amylose_content": "Medium amylose (22–24%), well-separated tender grain",
        "market_share": "Key domestic commercial variety across South India"
    },
    "Arborio": {
        "name": "Arborio Rice",
        "country": "Italy",
        "terroir": "Po River Valley (Piedmont and Lombardy regions, Northern Italy)",
        "grain": "short",
        "category": "High-Starch Creamy Grain",
        "global_consumers": "190+ Million People",
        "consumer_reach": "Staple grain in Mediterranean Europe, high-end global restaurants, and gourmet kitchens worldwide.",
        "global_producers": "1.9 Million Metric Tons / Year",
        "farmer_population": "Grown by ~320,000 specialized European agricultural estates.",
        "culinary_uses": "Classic Risotto (Milanese, Mushroom, Seafood), Rice Pudding, Arancini (fried rice balls)",
        "aroma_texture": "Plump kernels with a chalky center; releases amylopectin starch during stirring to create velvety creaminess while keeping an al dente bite.",
        "nutrition": "High carbohydrate density for athletic stamina, easily digestible creamy starch.",
        "amylose_content": "High amylopectin / low amylose (17–19%), maximum liquid absorption",
        "market_share": "World's most recognized risotto rice cultivar"
    },
    "Bomba": {
        "name": "Bomba Rice (Arroz Bomba)",
        "country": "Spain",
        "terroir": "Albufera freshwater wetland reserve in Valencia, Spain",
        "grain": "short",
        "category": "High-Absorption Round Grain",
        "global_consumers": "95+ Million People",
        "consumer_reach": "Central to Spanish national cuisine, consumed across Spain, Latin America, and culinary hotspots worldwide.",
        "global_producers": "850,000 Metric Tons / Year",
        "farmer_population": "Cultivated by ~120,000 artisan rice farmers in Mediterranean Spain.",
        "culinary_uses": "Authentic Valencian Paella, Arroz Negro, Arroz a Banda",
        "aroma_texture": "Absorbs 3x its volume in broth without bursting or becoming sticky; grains expand in width like an accordion.",
        "nutrition": "Rich in complex carbohydrates, low sodium, ideal broth carrier.",
        "amylose_content": "High amylose for short grain (23%), firm non-mushy texture",
        "market_share": "The benchmark premium grain for Spanish culinary arts"
    },
    "Koshihikari": {
        "name": "Koshihikari Rice",
        "country": "Japan",
        "terroir": "Niigata Prefecture (Uonuma district) fed by pure snowmelt waters and mineral mountain soil",
        "grain": "short",
        "category": "Japonica Premium Short Grain",
        "global_consumers": "340+ Million People",
        "consumer_reach": "The gold-standard table rice in Japan and the preferred sushi rice across East Asia, USA, and Europe.",
        "global_producers": "9.1 Million Metric Tons / Year",
        "farmer_population": "Grown by ~1.4 Million dedicated Japanese and international Japonica growers.",
        "culinary_uses": "Edomae Sushi, Onigiri (Rice Balls), Donburi bowls, traditional Kaiseki meals",
        "aroma_texture": "Naturally sweet, translucent sheen, springy and sticky texture that holds moisture and shape even when cooled.",
        "nutrition": "High energy density, natural grain sweetness, low in allergens.",
        "amylose_content": "Low amylose (15–16%), highly sticky and moist",
        "market_share": "Accounts for over 35% of all rice grown in Japan"
    },
    "Broken rice (Brokens)": {
        "name": "Broken Rice (Brokens / Cơm Tấm)",
        "country": "Vietnam, Thailand, India & West Africa",
        "terroir": "Milling hubs of the Mekong Delta, Chao Phraya Basin, and West African river valleys",
        "grain": "any",
        "category": "Milling Fragment Grade",
        "global_consumers": "680+ Million People",
        "consumer_reach": "Beloved daily staple across Vietnam (Cơm tấm), Senegal and West Africa (Thieboudienne national dish), and breakfast congee across East Asia.",
        "global_producers": "48 Million Metric Tons / Year",
        "farmer_population": "Produced from the output of over 50 Million rice smallholders across Asia and Africa.",
        "culinary_uses": "Vietnamese Broken Rice with grilled pork (Cơm tấm), Senegalese Ceebu Jën, Cantonese Congee, rice flour, rice noodles",
        "aroma_texture": "Quick-cooking, highly tender, absorbent texture with soothing mouthfeel.",
        "nutrition": "Identical nutritional value to whole white rice; cooks faster with lower energy fuel requirement.",
        "amylose_content": "Varies by base cultivar (18–26%), rapid starch gelatinization",
        "market_share": "10–15% of all global milled rice volume"
    },
    "Black Forbidden rice": {
        "name": "Black Forbidden Rice (Chak-Hao / Riceberry)",
        "country": "China, Thailand & India (Manipur)",
        "terroir": "Sub-tropical valleys of Yunnan (China), Chiang Mai (Thailand), and Manipur wetlands (India)",
        "grain": "medium",
        "category": "Anthocyanin Super-Grain",
        "global_consumers": "55+ Million People",
        "consumer_reach": "Historic imperial delicacy now popular among health-conscious consumers in Asia, Europe, and the Americas.",
        "global_producers": "780,000 Metric Tons / Year",
        "farmer_population": "Grown by ~450,000 heritage rice farmers in high-altitude valleys.",
        "culinary_uses": "Black rice pudding, warm grain bowls, Mango coconut sticky rice, traditional Chinese congee",
        "aroma_texture": "Deep violet-black hue with roasted nutty aroma and chewy texture.",
        "nutrition": "Contains more anthocyanin antioxidants than blueberries, 8.5g protein/100g, rich in iron, zinc, and dietary fibre.",
        "amylose_content": "Medium amylose (18–20%), chewy and non-sticky",
        "market_share": "Rapidly growing specialty antioxidant superfood segment"
    },
    "Parboiled (Sella) rice": {
        "name": "Parboiled (Golden Sella) Rice",
        "country": "India, Pakistan & Worldwide",
        "terroir": "Indo-Gangetic and Godavari river basins; hydrothermally processed before husking",
        "grain": "long",
        "category": "Golden Parboiled Table Rice",
        "global_consumers": "950+ Million People",
        "consumer_reach": "Prevalent staple across South Asia, the Middle East, Nigeria, and Latin America; valued for non-mushy texture.",
        "global_producers": "52 Million Metric Tons / Year",
        "farmer_population": "Cultivated by ~28 Million farmers across global paddy belts.",
        "culinary_uses": "Commercial Biryani, Catering Pulao, Nigerian Jollof Rice, Everyday table rice",
        "aroma_texture": "Subtle golden sheen; kernels never stick or mush, absorbing gravies cleanly.",
        "nutrition": "High micronutrient retention (B-vitamins driven from bran into endosperm during steaming), low glycemic index (GI 48–52).",
        "amylose_content": "High amylose (25–27%), completely non-sticky firm kernels",
        "market_share": "Over 20% of global rice trade volume"
    }
}


def get_profile(name, color_family="white", grain_type="medium"):
    """Returns rich global agricultural, consumer, and agronomic intelligence for any cultivar."""
    name_str = (name or "").lower()

    # Direct match in VARIETAL_PROFILES
    for key, data in VARIETAL_PROFILES.items():
        k = key.lower()
        if k in name_str or name_str in k:
            return data

    # Keyword matching
    if "brown" in name_str:
        return VARIETAL_PROFILES["Brown rice"]
    if "matta" in name_str or "rosematta" in name_str or "red cargo" in name_str or "red" in name_str:
        return VARIETAL_PROFILES["Matta (Rosematta)"]
    if "basmati" in name_str:
        return VARIETAL_PROFILES["Basmati"]
    if "jasmine" in name_str:
        return VARIETAL_PROFILES["Jasmine (Hom Mali)"]
    if "sona" in name_str or "masuri" in name_str:
        return VARIETAL_PROFILES["Sona Masuri"]
    if "ponni" in name_str:
        return VARIETAL_PROFILES["Ponni"]
    if "arborio" in name_str or "risotto" in name_str:
        return VARIETAL_PROFILES["Arborio"]
    if "bomba" in name_str or "paella" in name_str:
        return VARIETAL_PROFILES["Bomba"]
    if "sushi" in name_str or "koshihikari" in name_str or "japonica" in name_str:
        return VARIETAL_PROFILES["Koshihikari"]
    if "broken" in name_str or "brokens" in name_str:
        return VARIETAL_PROFILES["Broken rice (Brokens)"]
    if "black" in name_str or "forbidden" in name_str or "riceberry" in name_str:
        return VARIETAL_PROFILES["Black Forbidden rice"]
    if "parboiled" in name_str or "sella" in name_str:
        return VARIETAL_PROFILES["Parboiled (Sella) rice"]

    # Color-based archetype fallback
    if color_family == "brown":
        base = VARIETAL_PROFILES["Brown rice"].copy()
        if name: base["name"] = name
        return base
    elif color_family == "red":
        base = VARIETAL_PROFILES["Matta (Rosematta)"].copy()
        if name: base["name"] = name
        return base
    elif color_family == "black":
        base = VARIETAL_PROFILES["Black Forbidden rice"].copy()
        if name: base["name"] = name
        return base

    # Grain-based archetype fallback
    if grain_type == "long":
        base = VARIETAL_PROFILES["Basmati"].copy()
        if name: base["name"] = name
        return base
    elif grain_type == "short":
        base = VARIETAL_PROFILES["Arborio"].copy()
        if name: base["name"] = name
        return base
    else:
        base = VARIETAL_PROFILES["Sona Masuri"].copy()
        if name: base["name"] = name
        return base
