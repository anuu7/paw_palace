"""
Pet Health AI - Symptom Knowledge Base
========================================
Maps symptoms (keywords) to illnesses with weights per animal type.
Each entry: { "illness": str, "symptoms": [(keyword, weight), ...], "severity": str, "actions": [str,...] }
Weight scale: 0.1 (mild indicator) to 1.0 (strong indicator)
"""

DISEASE_KNOWLEDGE_BASE = {

    # ============================================================
    #  DOG CONDITIONS
    # ============================================================
    "dog": [
        {
            "illness": "Canine Parvovirus",
            "symptoms": [
                ("vomiting", 0.9), ("bloody stool", 0.9), ("lethargy", 0.8),
                ("loss of appetite", 0.8), ("fever", 0.7), ("dehydration", 0.7),
                ("diarrhea", 0.8), ("weight loss", 0.6), ("weakness", 0.7),
                ("sudden onset", 0.8), ("puppy", 0.7), ("not vaccinated", 0.6),
            ],
            "severity": "critical",
            "actions": [
                "Seek emergency veterinary care immediately",
                "Isolate from other dogs to prevent spread",
                "Maintain hydration - do not withhold food/water",
                "Expect intensive supportive care (IV fluids, antibiotics)",
                "Vaccination is the primary prevention",
            ],
            "description": "A highly contagious viral disease affecting puppies and unvaccinated dogs, causing severe gastrointestinal damage.",
        },
        {
            "illness": "Canine Distemper",
            "symptoms": [
                ("coughing", 0.8), ("nasal discharge", 0.8), ("fever", 0.7),
                ("lethargy", 0.8), ("loss of appetite", 0.7), ("vomiting", 0.6),
                ("diarrhea", 0.6), ("eye discharge", 0.7), ("seizures", 0.8),
                ("tremors", 0.7), ("hardened paw pads", 0.9), ("neurological", 0.7),
                ("not vaccinated", 0.7), ("young dog", 0.6),
            ],
            "severity": "critical",
            "actions": [
                "Immediate veterinary attention required",
                "Isolate from other dogs immediately",
                "Supportive care: fluids, antibiotics for secondary infections",
                "No specific cure - treatment is supportive",
                "Vaccination is essential prevention",
            ],
            "description": "A serious viral disease affecting respiratory, gastrointestinal, and nervous systems. Often fatal in puppies.",
        },
        {
            "illness": "Kennel Cough (Infectious Tracheobronchitis)",
            "symptoms": [
                ("persistent cough", 0.95), ("harsh barking cough", 0.9), ("gagging", 0.7),
                ("nasal discharge", 0.6), ("sneezing", 0.5), ("lethargy", 0.5),
                ("low fever", 0.4), ("loss of appetite", 0.4), ("runny nose", 0.5),
                ("honking cough", 0.8), ("kennel", 0.5), ("boarding", 0.5),
            ],
            "severity": "moderate",
            "actions": [
                "Most cases resolve on their own in 1-3 weeks",
                "Keep dog in humid environment",
                "Use harness instead of collar to reduce throat irritation",
                "Veterinary antibiotics if secondary infection develops",
                "Vaccinate against Bordetella (kennel cough vaccine)",
            ],
            "description": "A highly contagious respiratory infection common in dogs who have been in contact with other dogs (kennels, shelters, parks).",
        },
        {
            "illness": "Canine Leptospirosis",
            "symptoms": [
                ("vomiting", 0.7), ("lethargy", 0.7), ("loss of appetite", 0.7),
                ("increased thirst", 0.8), ("increased urination", 0.8), ("jaundice", 0.9),
                ("yellow eyes", 0.8), ("yellow gums", 0.8), ("fever", 0.6),
                ("muscle pain", 0.6), ("kidney pain", 0.7), ("bloody urine", 0.7),
                ("contact with rodents", 0.6), ("stagnant water", 0.5),
            ],
            "severity": "critical",
            "actions": [
                "Emergency veterinary care - zoonotic disease",
                "IV antibiotics and fluid therapy urgently needed",
                "Can damage kidneys and liver permanently",
                "Avoid contact with urine - human health risk",
                "Vaccination available and recommended in endemic areas",
            ],
            "description": "A bacterial infection spread through contact with infected animal urine, contaminated water, or soil. Zoonotic (spreads to humans).",
        },
        {
            "illness": "Canine Lyme Disease",
            "symptoms": [
                ("limping", 0.9), ("lameness", 0.8), ("joint swelling", 0.8),
                ("fever", 0.6), ("lethargy", 0.7), ("loss of appetite", 0.6),
                ("tick bite", 0.8), ("bull's eye rash", 0.7), ("swollen lymph nodes", 0.6),
                ("warm joints", 0.7), ("stiffness", 0.7), ("reluctant to move", 0.6),
                ("tick exposure", 0.7),
            ],
            "severity": "moderate",
            "actions": [
                "Veterinary consultation for proper diagnosis (blood test)",
                "Antibiotic treatment typically 4+ weeks",
                "Early treatment prevents chronic joint and kidney problems",
                "Use tick prevention products year-round",
                "Check for ticks after every outdoor activity",
            ],
            "description": "A tick-borne bacterial disease causing lameness, fever, and if untreated, chronic arthritis and kidney damage.",
        },
        {
            "illness": "Hot Spot (Acute Moist Dermatitis)",
            "symptoms": [
                ("red skin", 0.9), ("moist sores", 0.9), ("itching", 0.7),
                ("scratching", 0.8), ("licking", 0.8), ("hair loss", 0.6),
                ("painful", 0.6), ("swollen", 0.7), ("bleeding", 0.5),
                ("warm to touch", 0.8), ("sudden", 0.7), ("overnight", 0.6),
            ],
            "severity": "moderate",
            "actions": [
                "Clip hair around the affected area",
                "Clean with antiseptic solution",
                "Keep dog from licking/scratching (use e-collar)",
                "Topical antibiotic and steroid treatment",
                "Address underlying cause (allergies, fleas, matting)",
            ],
            "description": "A rapidly developing bacterial skin infection caused by self-trauma from scratching, licking, or biting. Common in hot, humid weather.",
        },
        {
            "illness": "Ear Infection (Otitis Externa)",
            "symptoms": [
                ("ear scratching", 0.9), ("head shaking", 0.9), ("ear odor", 0.8),
                ("discharge from ear", 0.8), ("red ear canal", 0.8), ("swollen ear", 0.7),
                ("painful ear", 0.7), ("brown discharge", 0.6), ("yellow discharge", 0.6),
                ("odor", 0.6), ("balance loss", 0.5), ("circling", 0.4),
            ],
            "severity": "moderate",
            "actions": [
                "Veterinary examination to identify cause (bacterial, fungal, yeast)",
                "Clean ear with veterinary-approved solution",
                "Apply prescribed ear drops as directed",
                "Do not use cotton swabs deep in ear canal",
                "Treat underlying allergy if recurrent",
            ],
            "description": "Inflammation of the outer ear canal, commonly caused by allergies, ear mites, bacteria, or yeast. Very common in floppy-eared breeds.",
        },
        {
            "illness": "Gastritis (Stomach Inflammation)",
            "symptoms": [
                ("vomiting", 0.9), ("nausea", 0.8), ("loss of appetite", 0.7),
                ("lethargy", 0.6), ("drooling", 0.7), ("abdominal pain", 0.7),
                ("gurgling stomach", 0.6), ("eating grass", 0.6), ("retching", 0.7),
                ("bloody vomit", 0.8), ("foam", 0.6),
            ],
            "severity": "moderate",
            "actions": [
                "Withhold food for 12-24 hours (adult dogs only)",
                "Offer small amounts of water frequently",
                "Introduce bland diet (boiled chicken and rice) slowly",
                "See vet if vomiting persists beyond 24 hours",
                "Seek immediate care for bloody vomit",
            ],
            "description": "Inflammation of the stomach lining, often caused by dietary indiscretion, infections, or toxins. Usually self-limiting in mild cases.",
        },
        {
            "illness": "Canine Hip Dysplasia",
            "symptoms": [
                ("difficulty standing", 0.8), ("limping", 0.8), ("reluctant to climb", 0.8),
                ("hip pain", 0.8), ("stiffness", 0.7), ("decreased activity", 0.7),
                ("bunny hopping", 0.9), ("narrow stance", 0.7), ("large breed", 0.6),
                ("older dog", 0.5), ("weight gain", 0.5),
            ],
            "severity": "moderate",
            "actions": [
                "Veterinary diagnosis via physical exam and X-rays",
                "Weight management is critical",
                "Joint supplements (glucosamine, chondroitin)",
                "Anti-inflammatory medications as prescribed",
                "Surgery may be required in severe cases",
            ],
            "description": "A hereditary developmental condition where the hip joint doesn't fit properly, leading to arthritis and pain. Common in large breeds.",
        },
        {
            "illness": "Flea Allergy Dermatitis",
            "symptoms": [
                ("intense itching", 0.9), ("scratching", 0.9), ("hair loss", 0.7),
                ("red bumps", 0.8), ("fleas", 0.8), ("flea dirt", 0.8),
                ("tail base", 0.8), ("back legs", 0.7), ("scabs", 0.7),
                ("skin infection", 0.6), ("licking", 0.6),
            ],
            "severity": "moderate",
            "actions": [
                "Apply veterinary-approved flea treatment to ALL pets",
                "Treat home environment (vacuum, wash bedding)",
                "Anti-itch medications and antibiotics if infected",
                "Flea prevention year-round recommended",
                "Allergic reaction can persist even with few fleas",
            ],
            "description": "An allergic reaction to flea saliva causing intense itching and skin damage, even from a single flea bite.",
        },
        {
            "illness": "Pancreatitis",
            "symptoms": [
                ("vomiting", 0.9), ("severe abdominal pain", 0.9), ("lethargy", 0.8),
                ("loss of appetite", 0.8), ("diarrhea", 0.7), ("hunched back", 0.8),
                ("fever", 0.6), ("dehydration", 0.6), ("fatty food", 0.5),
                ("swollen abdomen", 0.6),
            ],
            "severity": "critical",
            "actions": [
                "Immediate veterinary care - can be life-threatening",
                "Hospitalization typically required for IV fluids",
                "Withhold food initially (rest the pancreas)",
                "Low-fat diet essential for recovery and prevention",
                "Never feed fatty foods or table scraps",
            ],
            "description": "Inflammation of the pancreas, ranging from mild to severe. Often triggered by eating fatty foods. Can be life-threatening.",
        },
        {
            "illness": "Ringworm (Dermatophytosis)",
            "symptoms": [
                ("circular lesion", 0.9), ("bald patches", 0.8), ("scaly skin", 0.7),
                ("itching", 0.6), ("red ring", 0.8), ("crusty skin", 0.7),
                ("broken hair", 0.7), ("spreads", 0.6), ("contagious", 0.5),
            ],
            "severity": "low",
            "actions": [
                "Veterinary confirmation via fungal culture or UV light",
                "Oral antifungal medication for 6+ weeks",
                "Topical antifungal creams or shampoos",
                "Deep clean home environment",
                "Ringworm is contagious to humans - practice hygiene",
            ],
            "description": "A fungal skin infection causing circular, scaly patches with hair loss. Contagious to other animals and humans.",
        },
        {
            "illness": "Canine Rabies",
            "symptoms": [
                ("aggression", 0.8), ("drooling", 0.9), ("difficulty swallowing", 0.8),
                ("paralysis", 0.8), ("seizures", 0.7), ("behavior change", 0.8),
                ("fear of water", 0.7), ("confusion", 0.7), ("bite wound", 0.7),
                ("wild animal bite", 0.7), ("not vaccinated", 0.6),
            ],
            "severity": "critical",
            "actions": [
                "EMERGENCY: Contact health authorities immediately",
                "Rabies is fatal once symptoms appear",
                "Quarantine the animal if human exposure possible",
                "All pets must be vaccinated - required by law",
                "Post-exposure prophylaxis available for humans",
            ],
            "description": "A fatal viral disease affecting the central nervous system. Transmitted through saliva (bites) from infected animals. Always fatal once symptomatic.",
        },
        {
            "illness": "Allergic Dermatitis (Environmental)",
            "symptoms": [
                ("itching", 0.9), ("scratching", 0.9), ("red skin", 0.8),
                ("paw licking", 0.8), ("face rubbing", 0.8), ("ear infections", 0.7),
                ("seasonal", 0.7), ("pollen", 0.5), ("hot spots", 0.6),
                ("skin irritation", 0.7), ("hair loss", 0.5),
            ],
            "severity": "low",
            "actions": [
                "Veterinary dermatologist evaluation for allergy testing",
                "Antihistamines or corticosteroids for symptom relief",
                "Omega-3 fatty acid supplements",
                "Regular bathing with hypoallergenic shampoo",
                "Minimize exposure to known allergens",
            ],
            "description": "An immune system overreaction to environmental substances (pollen, dust, mold). Causes chronic itching and skin inflammation.",
        },
        {
            "illness": "Intestinal Parasites (Worms)",
            "symptoms": [
                ("weight loss", 0.7), ("pot belly", 0.7), ("scooting", 0.8),
                ("visible worms in stool", 0.9), ("rice grains around anus", 0.8),
                ("bloated", 0.6), ("lethargy", 0.5), ("loss of appetite", 0.5),
                ("diarrhea", 0.6), ("vomiting", 0.5), ("puppy", 0.6),
                ("worms in vomit", 0.9),
            ],
            "severity": "moderate",
            "actions": [
                "Veterinary fecal examination to identify parasite type",
                "Specific deworming medication based on parasite",
                "Puppies need multiple deworming treatments",
                "Clean up feces promptly to prevent spread",
                "Monthly heartworm prevention often includes intestinal coverage",
            ],
            "description": "Various intestinal worms (roundworms, tapeworms, hookworms, whipworms) that infect dogs through contaminated soil, feces, or prey animals.",
        },
        {
            "illness": "Heatstroke",
            "symptoms": [
                ("panting heavily", 0.9), ("excessive drooling", 0.9), ("red gums", 0.8),
                ("rapid heartbeat", 0.8), ("vomiting", 0.7), ("collapse", 0.9),
                ("confusion", 0.8), ("hot day", 0.7), ("car ride", 0.6),
                ("exercise in heat", 0.6), ("shallow breathing", 0.7),
            ],
            "severity": "critical",
            "actions": [
                "Move to cool area immediately",
                "Apply cool (not cold) water to body, especially neck, armpits, groin",
                "Offer small amounts of cool water to drink",
                "Seek emergency veterinary care - organ damage can occur",
                "Never leave dog in parked car, even briefly",
            ],
            "description": "Life-threatening overheating when body temperature exceeds 104°F. Common in hot cars, heavy exercise in heat, or brachycephalic breeds.",
        },
    ],

    # ============================================================
    #  CAT CONDITIONS
    # ============================================================
    "cat": [
        {
            "illness": "Feline Upper Respiratory Infection (URI)",
            "symptoms": [
                ("sneezing", 0.9), ("runny nose", 0.9), ("watery eyes", 0.8),
                ("congested", 0.7), ("loss of appetite", 0.7), ("lethargy", 0.6),
                ("fever", 0.6), ("coughing", 0.5), ("mouth ulcers", 0.6),
                ("eye discharge", 0.8), ("stertor", 0.6), ("shelter", 0.5),
                ("multiple cats", 0.6),
            ],
            "severity": "moderate",
            "actions": [
                "Keep cat in a warm, humidified room",
                "Clear nasal discharge with warm, damp cloth",
                "Encourage eating - try warming food slightly",
                "Antiviral or antibiotic treatment from vet as needed",
                "Most URIs resolve in 7-10 days",
            ],
            "description": "A common, highly contagious viral infection (similar to human cold) causing sneezing, nasal discharge, and eye problems. Common in shelters and multi-cat homes.",
        },
        {
            "illness": "Feline Leukemia Virus (FeLV)",
            "symptoms": [
                ("weight loss", 0.8), ("lethargy", 0.8), ("loss of appetite", 0.7),
                ("recurring infections", 0.8), ("gum inflammation", 0.7),
                ("anemia", 0.7), ("fever", 0.6), ("poor coat condition", 0.7),
                ("swollen lymph nodes", 0.6), ("stray cat", 0.5),
            ],
            "severity": "critical",
            "actions": [
                "Blood test (ELISA) for FeLV diagnosis",
                "No specific cure - treatment is supportive",
                "Keep infected cat indoors to prevent spread",
                "Regular veterinary monitoring for complications",
                "Vaccination available - test before vaccinating new cats",
            ],
            "description": "A retrovirus that causes cancer, immune suppression, and anemia. Transmitted through saliva, blood, and mother-to-kitten. No cure but manageable.",
        },
        {
            "illness": "Feline Panleukopenia (Feline Distemper)",
            "symptoms": [
                ("vomiting", 0.8), ("bloody diarrhea", 0.9), ("lethargy", 0.9),
                ("fever", 0.7), ("loss of appetite", 0.8), ("dehydration", 0.7),
                ("sudden death", 0.7), ("kittens", 0.6), ("not vaccinated", 0.7),
                ("hiding", 0.6),
            ],
            "severity": "critical",
            "actions": [
                "EMERGENCY: Seek veterinary care immediately",
                "Intensive IV fluid therapy essential",
                "Antibiotics to prevent secondary infections",
                "Strict isolation from other cats",
                "Vaccination provides excellent protection",
            ],
            "description": "A highly contagious and often fatal viral disease causing severe vomiting, diarrhea, and immune system collapse. Also called feline distemper.",
        },
        {
            "illness": "Feline Diabetes Mellitus",
            "symptoms": [
                ("increased thirst", 0.9), ("increased urination", 0.9), ("weight loss", 0.8),
                ("increased appetite", 0.7), ("lethargy", 0.7), ("cloudy eyes", 0.5),
                ("obesity", 0.6), ("weakness", 0.6), ("poor coat", 0.6),
                ("older cat", 0.5),
            ],
            "severity": "high",
            "actions": [
                "Veterinary diagnosis via blood and urine tests",
                "Insulin injections or oral medications as prescribed",
                "Dietary management: high-protein, low-carb diet",
                "Regular glucose monitoring at home",
                "Weight management is crucial for recovery",
            ],
            "description": "A metabolic disorder where the body cannot regulate blood sugar properly. Often associated with obesity. Can be managed with treatment.",
        },
        {
            "illness": "Feline Urinary Tract Disease (FLUTD)",
            "symptoms": [
                ("straining to urinate", 0.9), ("blood in urine", 0.9), ("crying when urinating", 0.9),
                ("frequent urination", 0.8), ("urinating outside litter box", 0.8),
                ("licking genital area", 0.7), ("male cat", 0.6), ("blocked", 0.8),
                ("no urine production", 0.9), ("vomiting", 0.5),
            ],
            "severity": "critical",
            "actions": [
                "URGENT: Blocked cats can die within 24-48 hours - seek immediate care",
                "Urinary catheter may be needed for blocked cats",
                "Increase water intake - wet food helps",
                "Reduce stress - FLUTD is often stress-related",
                "Special urinary diet may be prescribed long-term",
            ],
            "description": "Inflammation of the urinary tract. Male cats can develop life-threatening urethral blockages. Symptoms include straining and blood in urine.",
        },
        {
            "illness": "Ear Mites (Otodectes cynotis)",
            "symptoms": [
                ("ear scratching", 0.9), ("head shaking", 0.8), ("dark discharge in ear", 0.9),
                ("coffee-ground ear wax", 0.9), ("ear odor", 0.7), ("red ears", 0.7),
                ("scabs around ears", 0.6), ("inner ear inflammation", 0.7),
            ],
            "severity": "low",
            "actions": [
                "Veterinary examination to confirm mites",
                "Prescription ear drops or topical treatment",
                "Clean ears with veterinary-approved solution",
                "Treat all pets in household",
                "Mites are highly contagious between cats",
            ],
            "description": "Microscopic parasitic mites that live in the ear canal, causing intense itching and dark crumbly discharge. Very common in kittens.",
        },
        {
            "illness": "Hyperthyroidism",
            "symptoms": [
                ("weight loss", 0.9), ("increased appetite", 0.8), ("hyperactivity", 0.7),
                ("vomiting", 0.7), ("diarrhea", 0.6), ("increased thirst", 0.7),
                ("matted fur", 0.6), ("rapid heart rate", 0.7), ("older cat", 0.6),
                ("unkempt appearance", 0.7),
            ],
            "severity": "high",
            "actions": [
                "Blood test to check thyroid hormone levels",
                "Treatment options: medication, radioactive iodine, surgery, or diet",
                "Medication (methimazole) controls symptoms effectively",
                "Regular monitoring of kidney function needed",
                "Most cats respond well to treatment",
            ],
            "description": "Overproduction of thyroid hormone, typically from a benign tumor. Most common in cats over 8 years old. Highly manageable with treatment.",
        },
        {
            "illness": "Feline Conjunctivitis",
            "symptoms": [
                ("red eyes", 0.9), ("eye discharge", 0.9), ("squinting", 0.8),
                ("pawing at eyes", 0.7), ("swollen eyes", 0.7), ("watery eyes", 0.7),
                ("crusty eyes", 0.6), ("third eyelid visible", 0.7),
            ],
            "severity": "low",
            "actions": [
                "Keep eyes clean with warm, damp cloth",
                "Veterinary eye examination",
                "Topical antibiotic or antiviral eye drops as prescribed",
                "Address underlying URI if present",
                "Isolate from other cats if contagious",
            ],
            "description": "Inflammation of the eye membrane, commonly caused by viral or bacterial infections. Usually resolves with treatment.",
        },
        {
            "illness": "Hairballs",
            "symptoms": [
                ("coughing", 0.7), ("retching", 0.8), ("vomiting hair", 0.9),
                ("hacking", 0.8), ("loss of appetite", 0.4), ("constipation", 0.6),
                ("lethargy", 0.3), ("long-haired", 0.6), ("excessive grooming", 0.6),
            ],
            "severity": "low",
            "actions": [
                "Hairball remedies (laxatives) to help pass hair",
                "Regular brushing to reduce loose fur ingestion",
                "Hairball-control cat food",
                "Increase fiber intake",
                "See vet if vomiting persists or cat seems constipated",
            ],
            "description": "Accumulated fur in the stomach from grooming. Cats normally pass or vomit hairballs. Frequent hairballs may indicate other issues.",
        },
        {
            "illness": "Feline Chronic Kidney Disease (CKD)",
            "symptoms": [
                ("increased thirst", 0.9), ("increased urination", 0.9), ("weight loss", 0.8),
                ("lethargy", 0.8), ("poor appetite", 0.7), ("vomiting", 0.7),
                ("bad breath", 0.6), ("older cat", 0.6), ("weight loss despite eating", 0.7),
            ],
            "severity": "high",
            "actions": [
                "Blood and urine tests for diagnosis",
                "Special kidney-friendly diet (low protein, low phosphorus)",
                "Fluid therapy to prevent dehydration",
                "Medications to manage symptoms",
                "Regular monitoring every 3-6 months",
            ],
            "description": "Progressive, irreversible kidney damage most common in senior cats. Early detection and management can significantly extend quality of life.",
        },
        {
            "illness": "Ringworm (Dermatophytosis) in Cats",
            "symptoms": [
                ("circular bald patches", 0.9), ("scaly skin", 0.8), ("broken hair", 0.8),
                ("red patches", 0.7), ("itching", 0.5), ("crusty lesions", 0.7),
                ("head lesions", 0.7), ("ears affected", 0.6),
            ],
            "severity": "low",
            "actions": [
                "Veterinary confirmation via fungal culture",
                "Oral antifungal medication for 6+ weeks",
                "Topical antifungal creams or dips",
                "Deep clean home environment",
                "Ringworm is contagious to other pets and humans",
            ],
            "description": "A fungal skin infection causing circular patches of hair loss. Common in kittens and stray cats. Contagious to other animals and humans.",
        },
    ],

    # ============================================================
    #  BIRD CONDITIONS
    # ============================================================
    "bird": [
        {
            "illness": "Avian Chlamydiosis (Psittacosis / Parrot Fever)",
            "symptoms": [
                ("fluffed feathers", 0.8), ("lethargy", 0.8), ("loss of appetite", 0.8),
                ("weight loss", 0.7), ("eye discharge", 0.6), ("nasal discharge", 0.7),
                ("diarrhea", 0.7), ("green droppings", 0.8), ("respiratory signs", 0.7),
                ("human flu symptoms", 0.6),
            ],
            "severity": "high",
            "actions": [
                "Seek avian veterinarian care immediately",
                "Zoonotic - humans can contract this illness",
                "Doxycycline antibiotic treatment for 45 days",
                "Quarantine and disinfect cage thoroughly",
                "Human symptoms: fever, headache, cough - see doctor",
            ],
            "description": "A bacterial infection (Chlamydia psittaci) transmissible from birds to humans. Also called Psittacosis or Parrot Fever. Causes flu-like symptoms.",
        },
        {
            "illness": "Respiratory Infection (Aspergillosis)",
            "symptoms": [
                ("labored breathing", 0.9), ("open-mouth breathing", 0.9), ("sneezing", 0.7),
                ("nasal discharge", 0.7), ("lethargy", 0.7), ("loss of appetite", 0.6),
                ("tail bobbing", 0.8), ("wheezing", 0.7), ("moldy environment", 0.5),
            ],
            "severity": "high",
            "actions": [
                "Seek avian veterinarian care immediately",
                "Antifungal medication (itraconazole or amphotericin B)",
                "Remove bird from damp, moldy environments",
                "Improve cage ventilation",
                "Can be chronic and difficult to treat",
            ],
            "description": "A fungal infection of the respiratory system, often from moldy seeds, damp bedding, or poor ventilation. Common in birds with weakened immune systems.",
        },
        {
            "illness": "Psittacine Beak and Feather Disease (PBFD)",
            "symptoms": [
                ("feather loss", 0.9), ("abnormal feathers", 0.9), ("beak abnormalities", 0.8),
                ("beak overgrowth", 0.7), ("deformed beak", 0.7), ("immune suppressed", 0.7),
                ("young parrot", 0.6), ("recurring infections", 0.6),
            ],
            "severity": "critical",
            "actions": [
                "Blood test for PBFD virus confirmation",
                "No specific cure - disease is usually progressive",
                "Supportive care and treat secondary infections",
                "Strict quarantine of infected birds",
                "Avoid acquiring birds from unknown sources",
            ],
            "description": "A viral disease causing feather abnormalities, beak deformities, and immune suppression. Highly contagious among psittacine birds. Often fatal.",
        },
        {
            "illness": "Avian Goiter (Iodine Deficiency)",
            "symptoms": [
                ("enlarged thyroid", 0.8), ("difficulty swallowing", 0.8), ("crop problems", 0.7),
                ("labored breathing", 0.7), ("lethargy", 0.6), ("poor feather quality", 0.5),
                ("seed-only diet", 0.6), ("gurgling sounds", 0.7),
            ],
            "severity": "moderate",
            "actions": [
                "Avian veterinarian examination",
                "Iodine supplementation in water or food",
                "Switch to formulated pellet diet",
                "Include vegetables and fruits in diet",
                "Most common in budgerigars on all-seed diets",
            ],
            "description": "Thyroid gland enlargement due to iodine deficiency, common in seed-only diets. Causes breathing and swallowing difficulties.",
        },
        {
            "illness": "Candidiasis (Yeast Infection)",
            "symptoms": [
                ("white patches in mouth", 0.9), ("crop impaction", 0.7), ("loss of appetite", 0.7),
                ("regurgitation", 0.7), ("lethargy", 0.6), ("sour crop smell", 0.8),
                ("weight loss", 0.6), ("diarrhea", 0.5),
            ],
            "severity": "moderate",
            "actions": [
                "Veterinary examination and culture",
                "Antifungal medication (nystatin or fluconazole)",
                "Probiotics to restore healthy gut flora",
                "Improve hygiene and cage sanitation",
                "Often secondary to antibiotic use or stress",
            ],
            "description": "A yeast (Candida) overgrowth in the digestive tract, often triggered by antibiotics, stress, or poor nutrition. Creates white mouth lesions.",
        },
        {
            "illness": "Vitamin A Deficiency",
            "symptoms": [
                ("white spots in mouth", 0.8), ("nasal discharge", 0.7), ("eye problems", 0.7),
                ("poor feather quality", 0.7), ("lethargy", 0.6), ("loss of appetite", 0.6),
                ("seed-only diet", 0.7), ("squinting", 0.6),
            ],
            "severity": "moderate",
            "actions": [
                "Veterinary diagnosis and Vitamin A injection if severe",
                "Dietary supplementation (cod liver oil, carrots, leafy greens)",
                "Switch to formulated pellet diet",
                "Vitamin A supplementation for 2-4 weeks",
                "Prevention through balanced diet",
            ],
            "description": "Common in seed-only fed birds. Causes mucosal problems, eye issues, and respiratory infections. Seeds lack essential vitamin A.",
        },
        {
            "illness": " feather Destructive Behavior (Feather Plucking)",
            "symptoms": [
                ("feather plucking", 0.95), ("bald patches", 0.9), ("skin damage", 0.8),
                ("self-mutilation", 0.9), ("stressed bird", 0.7), ("boredom", 0.6),
                ("lonely", 0.5), ("cage-bound", 0.5), ("attention-seeking", 0.4),
            ],
            "severity": "moderate",
            "actions": [
                "Rule out medical causes first (skin parasites, allergies)",
                "Address environmental enrichment needs",
                "Increase interaction and out-of-cage time",
                "Provide foraging toys and activities",
                "Consult avian behavior specialist",
            ],
            "description": "A behavioral disorder where birds excessively pluck or chew their own feathers. Can have medical or psychological causes. Requires thorough investigation.",
        },
    ],

    # ============================================================
    #  RABBIT CONDITIONS
    # ============================================================
    "rabbit": [
        {
            "illness": "Snuffles (Pasteurella multocida Infection)",
            "symptoms": [
                ("sneezing", 0.9), ("nasal discharge", 0.9), ("snuffling sounds", 0.9),
                ("matted front paws", 0.8), ("weepy eyes", 0.7), ("lethargy", 0.6),
                ("loss of appetite", 0.5), ("wheezing", 0.6),
            ],
            "severity": "moderate",
            "actions": [
                "Veterinary examination and culture",
                "Antibiotic treatment (avoid penicillin-type in gut flora)",
                "Keep rabbit in clean, dust-free environment",
                "Remove irritants (cedar/pine shavings)",
                "Can become chronic - manage flare-ups",
            ],
            "description": "A bacterial respiratory infection, similar to a cold in humans. Named for the snuffling breathing sounds. Can be chronic.",
        },
        {
            "illness": "Gastrointestinal Stasis (GI Stasis)",
            "symptoms": [
                ("not eating", 0.9), ("no droppings", 0.9), ("hunched posture", 0.8),
                ("lethargy", 0.8), ("abdominal pain", 0.7), ("small droppings", 0.7),
                ("grinding teeth", 0.7), ("bloated", 0.6), ("refusing treats", 0.6),
            ],
            "severity": "critical",
            "actions": [
                "URGENT: Rabbits can die within 24 hours of not eating",
                "Offer hay immediately - fresh Timothy hay is essential",
                "Gentle belly massage in circular motions",
                "Encourage movement to stimulate gut",
                "Immediate vet visit - may need fluid therapy and critical care feeding",
            ],
            "description": "A life-threatening slowdown or complete stop of the digestive system. Caused by stress, dehydration, pain, or diet. Medical emergency.",
        },
        {
            "illness": "Encephalitozoon cuniculi (E. cuniculi)",
            "symptoms": [
                ("head tilt", 0.9), ("circling", 0.9), ("loss of balance", 0.9),
                ("tremors", 0.7), ("cataracts", 0.7), ("kidney failure", 0.6),
                ("paralysis", 0.7), ("weight loss", 0.5),
            ],
            "severity": "high",
            "actions": [
                "Blood test or MRI for diagnosis",
                "Antiparasitic medication (albendazole or fenbendazole)",
                "Supportive care for neurological symptoms",
                "Strict quarantine - spreads through urine",
                "Disinfect environment with bleach solution",
            ],
            "description": "A microscopic parasite causing neurological symptoms (head tilt, circling), kidney damage, and eye problems. Spread through infected urine.",
        },
        {
            "illness": "Flystrike (Myiasis)",
            "symptoms": [
                ("maggots", 0.95), ("soiled fur", 0.8), ("lethargy", 0.7),
                ("loss of appetite", 0.7), ("shock", 0.8), ("foul smell", 0.8),
                ("hot weather", 0.6), ("dirty hutch", 0.7), ("weak rabbit", 0.6),
            ],
            "severity": "critical",
            "actions": [
                "EMERGENCY: Seek immediate veterinary care",
                "Clip fur and remove all maggots",
                "Wound cleaning and antibiotic treatment",
                "Fluid therapy and pain management",
                "Prevention: keep hutches clean, check rabbits twice daily in summer",
            ],
            "description": "Flies lay eggs on soiled fur (especially around the rear). Maggots then burrow into skin, releasing toxins. Can be fatal within hours.",
        },
        {
            "illness": "Dental Disease (Malocclusion)",
            "symptoms": [
                ("drooling", 0.9), ("wet chin", 0.9), ("not eating", 0.7),
                ("weight loss", 0.7), ("difficulty chewing", 0.8), ("dropping food", 0.7),
                ("teeth overgrown", 0.8), ("spikes on teeth", 0.7), ("eye discharge", 0.6),
            ],
            "severity": "moderate",
            "actions": [
                "Veterinary dental examination under anesthesia",
                "Teeth filing or trimming as needed",
                "Provide unlimited hay for natural tooth wear",
                "Regular dental check-ups every 6 months",
                "Diet adjustment: more hay, fewer pellets",
            ],
            "description": "Rabbit teeth grow continuously. Malocclusion causes overgrowth, spikes, and pain. Managed by regular filing and diet control.",
        },
        {
            "illness": "Uterine Cancer (Adenocarcinoma)",
            "symptoms": [
                ("blood in urine", 0.8), ("aggressive behavior", 0.6), ("lethargy", 0.6),
                ("poor appetite", 0.6), ("weight loss", 0.6), ("female rabbit", 0.7),
                ("over 4 years old", 0.6), ("lumps in abdomen", 0.5),
            ],
            "severity": "critical",
            "actions": [
                "Spaying is the best prevention (80%+ of unspayed females develop tumors)",
                "Veterinary examination and ultrasound",
                "Surgical removal if caught early",
                "Annual check-ups for older unspayed females",
                "Early spaying prevents this cancer entirely",
            ],
            "description": "Uterine cancer is extremely common in unspayed female rabbits over 4 years. Spaying before 2 years of age prevents this cancer.",
        },
        {
            "illness": "E. cuniculi (Kidney Infection in Rabbits)",
            "symptoms": [
                ("head tilt", 0.8), ("circling", 0.8), ("cataracts", 0.7),
                ("white spots on eyes", 0.7), ("kidney failure", 0.6), ("lethargy", 0.6),
                ("weight loss", 0.5), ("poor appetite", 0.5),
            ],
            "severity": "high",
            "actions": [
                "Blood tests and ultrasound for diagnosis",
                "Antiparasitic medication (fenbendazole)",
                "Supportive care for neurological symptoms",
                "Kidney support supplements",
                "Regular monitoring of kidney function",
            ],
            "description": "A parasitic infection affecting kidneys, eyes, and nervous system. Causes head tilt, cataracts, and kidney failure. Spread through urine.",
        },
    ],

    # ============================================================
    #  HAMSTER CONDITIONS
    # ============================================================
    "hamster": [
        {
            "illness": "Wet Tail (Proliferative Ileitis)",
            "symptoms": [
                ("wet tail", 0.95), ("diarrhea", 0.9), ("lethargy", 0.8),
                ("loss of appetite", 0.8), ("hunched posture", 0.7), ("matted fur", 0.8),
                ("death", 0.7), ("young hamster", 0.6), ("stress", 0.5),
            ],
            "severity": "critical",
            "actions": [
                "EMERGENCY: Seek veterinary care immediately",
                "This disease can kill within 48 hours",
                "Antibiotics and fluid therapy urgently needed",
                "Isolate affected hamster from others",
                "Reduce stress and improve cage hygiene",
            ],
            "description": "A severe, often fatal bacterial disease causing watery diarrhea and rapid dehydration. Most common in young hamsters under stress.",
        },
        {
            "illness": "Respiratory Infection",
            "symptoms": [
                ("sneezing", 0.8), ("runny nose", 0.8), ("labored breathing", 0.9),
                ("wheezing", 0.8), ("lethargy", 0.6), ("loss of appetite", 0.6),
                ("wet fur around nose", 0.7), ("clicking sounds", 0.7),
            ],
            "severity": "moderate",
            "actions": [
                "Keep hamster warm (85°F / 29°C ideal)",
                "Increase humidity in the room",
                "Veterinary examination for antibiotics if needed",
                "Remove dusty bedding - use paper-based bedding",
                "Avoid strong smells near cage (perfumes, cleaners)",
            ],
            "description": "Bacterial respiratory infections common in hamsters from drafts, dusty bedding, or strong odors. Can progress to pneumonia if untreated.",
        },
        {
            "illness": "Tumors (Cancerous and Non-cancerous)",
            "symptoms": [
                ("lumps", 0.9), ("weight loss", 0.7), ("lethargy", 0.6),
                ("difficulty moving", 0.6), ("loss of appetite", 0.5),
                ("older hamster", 0.5), ("visible growth", 0.8),
            ],
            "severity": "high",
            "actions": [
                "Veterinary examination to assess lump",
                "Surgical removal if tumor is accessible",
                "Many lumps in older hamsters are benign",
                "Pain management if inoperable",
                "Quality of life assessment with vet",
            ],
            "description": "Tumors are very common in older hamsters. Can be benign (lipomas, cysts) or malignant. Early veterinary assessment is important.",
        },
        {
            "illness": "Diabetes Mellitus",
            "symptoms": [
                ("increased thirst", 0.9), ("increased urination", 0.9), ("weight loss", 0.7),
                ("lethargy", 0.6), ("cloudy eyes", 0.6), ("genetics", 0.5),
                ("Chinese hamster", 0.6),
            ],
            "severity": "high",
            "actions": [
                "Blood glucose test by veterinarian",
                "Diet change: remove sugary treats and fruits",
                "High-protein, high-fiber diet",
                "Monitor water intake and weight",
                "Some cases managed with insulin",
            ],
            "description": "Diabetes is relatively common in certain hamster breeds (especially Chinese). Managed through diet modification and sometimes insulin.",
        },
        {
            "illness": "Fungal Infection (Ringworm)",
            "symptoms": [
                ("hair loss", 0.8), ("circular lesions", 0.8), ("scaly skin", 0.7),
                ("itching", 0.6), ("red skin", 0.6), ("crusty patches", 0.7),
                ("spreading lesions", 0.6),
            ],
            "severity": "low",
            "actions": [
                "Veterinary confirmation (skin scraping or UV light)",
                "Antifungal cream or oral medication",
                "Disinfect cage and all accessories",
                "Ringworm is contagious to humans - handle with gloves",
                "Keep affected hamster isolated during treatment",
            ],
            "description": "A fungal skin infection causing circular patches of hair loss. Transmissible to humans. Common in young hamsters and those in poor conditions.",
        },
    ],

    # ============================================================
    #  FISH CONDITIONS
    # ============================================================
    "fish": [
        {
            "illness": "Ich (White Spot Disease)",
            "symptoms": [
                ("white spots", 0.95), ("itching", 0.8), ("flashing", 0.9),
                ("scraping against objects", 0.9), ("clamped fins", 0.7),
                ("lethargy", 0.6), ("loss of appetite", 0.5), ("mortality", 0.6),
                ("sudden death", 0.5),
            ],
            "severity": "high",
            "actions": [
                "Raise water temperature gradually (for tropical fish)",
                "Aquarium salt treatment",
                "Malachite green or formalin-based medication",
                "Treat entire tank - Ich has a free-swimming stage",
                "Complete 3-day treatment course minimum",
            ],
            "description": "The most common fish disease. Caused by a parasitic protozoan (Ichthyophthirius multifiliis). Presents as white salt-like spots on skin and fins.",
        },
        {
            "illness": "Fin Rot",
            "symptoms": [
                ("fin deterioration", 0.9), ("ragged fins", 0.9), ("red edges", 0.7),
                ("black edges", 0.6), ("fuzzy fins", 0.7), ("poor water quality", 0.6),
                ("injured fish", 0.5), ("cloudy water", 0.4),
            ],
            "severity": "moderate",
            "actions": [
                "Test and correct water quality immediately",
                "Partial water change (25-50%)",
                "Aquarium salt added to tank",
                "Antibacterial medication if advanced",
                "Remove sharp decorations that could cause injury",
            ],
            "description": "Bacterial infection causing deterioration of fins and tail. Almost always secondary to poor water quality or injury. Common in bettas and goldfish.",
        },
        {
            "illness": "Dropsy (Fluid Retention)",
            "symptoms": [
                ("bloated", 0.9), ("raised scales", 0.9), ("pinecone appearance", 0.9),
                ("swollen belly", 0.8), ("lethargy", 0.7), ("loss of appetite", 0.7),
                ("pale gills", 0.6), ("eyes protruding", 0.7),
            ],
            "severity": "critical",
            "actions": [
                "Isolate affected fish immediately",
                "Epsom salt bath treatment",
                "Antibacterial food or medication",
                "Test water quality - usually underlying cause",
                "Often fatal - focus on prevention via water quality",
            ],
            "description": "A severe condition where fluid accumulates in the body cavity, causing scales to protrude like a pinecone. Usually indicates organ failure.",
        },
        {
            "illness": "Swim Bladder Disorder",
            "symptoms": [
                ("floating lopsided", 0.9), ("sinking to bottom", 0.8), ("swimming upside down", 0.9),
                ("can't swim properly", 0.9), ("bloated", 0.6), ("goldfish", 0.5),
                ("betta", 0.5), ("constipation", 0.6),
            ],
            "severity": "moderate",
            "actions": [
                "Fast the fish for 2-3 days",
                "Then feed blanched peas (skinned)",
                "Reduce water level to ease swimming effort",
                "Check temperature is appropriate for species",
                "Avoid overfeeding - a common cause",
            ],
            "description": "The swim bladder (gas-filled organ for buoyancy) isn't working properly. Fish float oddly or sink. Common in fancy goldfish and bettas.",
        },
        {
            "illness": "Anchor Worms (Lernaea)",
            "symptoms": [
                ("visible worms", 0.9), ("thread-like parasites", 0.9), ("red inflammation", 0.8),
                ("scratching", 0.7), ("lethargy", 0.6), ("mucus excess", 0.6),
                ("ulcers near parasite", 0.7),
            ],
            "severity": "moderate",
            "actions": [
                "Carefully remove visible worms with tweezers",
                "Apply potassium permanganate or清凉油 to wound",
                "Salt bath treatment for entire tank",
                "Antibacterial treatment for secondary infections",
                "Quarantine new fish to prevent introduction",
            ],
            "description": "Parasitic crustaceans that embed into fish flesh, appearing as thin greenish-white threads. Causes inflammation and secondary infections.",
        },
        {
            "illness": "Ammonia Poisoning",
            "symptoms": [
                ("gasping at surface", 0.9), ("red or purple gills", 0.9), ("lethargy", 0.8),
                ("no appetite", 0.7), ("burns on body", 0.7), ("new tank", 0.6),
                ("overstocked", 0.6), ("cloudy water", 0.4),
            ],
            "severity": "critical",
            "actions": [
                "IMMEDIATE large water change (30-50%)",
                "Test ammonia levels with test kit",
                "Add beneficial bacteria (filter booster)",
                "Do not overfeed - remove uneaten food",
                "Reduce fish population if overstocked",
            ],
            "description": "Ammonia builds up from fish waste and decomposing food. Causes chemical burns to gills and skin. Often occurs in new tanks or overcrowded tanks.",
        },
    ],

    # ============================================================
    #  REPTILE CONDITIONS
    # ============================================================
    "reptile": [
        {
            "illness": "Metabolic Bone Disease (MBD)",
            "symptoms": [
                ("soft bones", 0.9), ("bending legs", 0.9), ("rubbery jaw", 0.9),
                ("difficulty walking", 0.8), ("seizures", 0.7), ("twitching", 0.7),
                ("lethargy", 0.6), ("no UVB light", 0.7), ("poor diet", 0.6),
                ("lizard", 0.5), ("turtle", 0.5),
            ],
            "severity": "critical",
            "actions": [
                "Immediate veterinary care for calcium injection",
                "Provide UVB lighting 10-12 hours daily",
                "Calcium and vitamin D3 supplementation",
                "Improve diet with calcium-rich foods",
                "Can cause permanent skeletal deformities if untreated",
            ],
            "description": "Calcium deficiency causing weak, deformed bones. Caused by lack of UVB light, poor diet, or improper temperatures. Common in bearded dragons and leopard geckos.",
        },
        {
            "illness": "Respiratory Infection in Reptiles",
            "symptoms": [
                ("gasping", 0.9), ("mouth breathing", 0.9), ("wheezing", 0.8),
                ("mucus from mouth", 0.8), ("lethargy", 0.7), ("loss of appetite", 0.6),
                ("bubbles from nose", 0.8), ("coughing", 0.7), ("open-mouth breathing", 0.9),
            ],
            "severity": "high",
            "actions": [
                "Veterinary examination and possibly X-rays",
                "Nebulized antibiotics may be needed",
                "Raise enclosure temperature (species-appropriate)",
                "Improve humidity control",
                "Ensure proper ventilation in enclosure",
            ],
            "description": "Bacterial or viral respiratory infections common in reptiles kept in incorrect humidity or temperature. Can develop into pneumonia.",
        },
        {
            "illness": "Mite Infestation",
            "symptoms": [
                ("tiny black dots", 0.9), ("mites on skin", 0.9), ("restlessness", 0.7),
                ("soaking frequently", 0.8), ("dark spots in joints", 0.8),
                ("anemia", 0.6), ("lethargy", 0.5), ("depression", 0.5),
            ],
            "severity": "moderate",
            "actions": [
                "Veterinary-grade mite treatment (permethrin-based)",
                "Complete enclosure disinfection",
                "Treat all reptiles in household",
                "Replace substrate completely",
                "Repeat treatment in 2 weeks to kill hatched eggs",
            ],
            "description": "Blood-feeding mites that appear as tiny black or red dots. Cause stress, anemia, and can transmit diseases. Common on snakes and lizards.",
        },
        {
            "illness": "Scale Rot",
            "symptoms": [
                ("blisters", 0.9), ("ulcers on scales", 0.9), ("reddish scales", 0.8),
                ("mushy scales", 0.9), ("snake", 0.6), ("dirty enclosure", 0.7),
                ("wet substrate", 0.7), ("foul smell", 0.6),
            ],
            "severity": "high",
            "actions": [
                "Clean and dry the enclosure completely",
                "Topical antibiotic treatment on wounds",
                "Remove damp substrate immediately",
                "Improve enclosure hygiene",
                "Veterinary care for severe cases",
            ],
            "description": "Bacterial infection causing blister-like lesions and ulcers, usually on the belly scales. Caused by dirty, damp enclosure conditions.",
        },
        {
            "illness": "Impaction (Blocked Intestines)",
            "symptoms": [
                ("not defecating", 0.9), ("bloated", 0.8), ("lethargy", 0.7),
                ("no appetite", 0.7), ("straining", 0.8), ("giant leopard gecko", 0.5),
                ("improper substrate", 0.6), ("loose substrate", 0.5),
            ],
            "severity": "high",
            "actions": [
                "Warm bath and gentle belly massage",
                "Increase enclosure temperature",
                "Offer olive oil or reptile-safe laxative",
                "Remove loose substrate (calcium sand especially dangerous)",
                "See vet if no improvement within 24-48 hours",
            ],
            "description": "Intestinal blockage from ingested substrate, parasites, or food. Common in lizards and geckos on inappropriate loose substrates.",
        },
    ],
}


# ============================================================
#  GLOBAL / CROSS-SPECIES SYMPTOMS
# ============================================================
GENERAL_SYMPTOMS = [
    "lethargy", "loss of appetite", "weight loss", "fever", "vomiting",
    "diarrhea", "dehydration", "weakness", "collapse", "shock",
]


def get_knowledge_base(animal_type: str) -> list:
    """Return the disease list for a given animal type."""
    return DISEASE_KNOWLEDGE_BASE.get(animal_type.lower(), [])


def get_all_symptom_keywords(animal_type: str) -> list:
    """Extract all unique symptom keywords for an animal type."""
    kb = get_knowledge_base(animal_type)
    keywords = set()
    for disease in kb:
        for symptom, weight in disease["symptoms"]:
            keywords.add(symptom.lower())
    return sorted(keywords)
