"""
KEYWORDS maps each knowledge module to the words/phrases that signal a
question belongs to it. classifier.py uses this to score a question
against every module and pick the best match.

This is exactly the dictionary you already built — kept as-is, just
given its own file so classifier.py can import it cleanly.
"""

KEYWORDS = {

"finance": [
    "investment", "budget", "roi", "profit", "loss", "net margin", "funding",
    "loan", "discount", "cash", "money", "revenue", "price", "gross profit",
    "selling price", "operating expenses", "cost price", "cash flow",
    "expenses", "emergency fund", "interest", "income", "working capital",
    "inventory cost", "break even"
],

"marketing": [
    "branding", "brand", "brand identity", "business name", "logo", "tagline",
    "marketing", "marketing strategy", "marketing funnel", "advertisement",
    "advertising", "promotion", "promote", "digital marketing",
    "online marketing", "offline marketing", "social media",
    "social media marketing", "instagram", "facebook", "youtube", "linkedin",
    "whatsapp marketing", "content marketing", "influencer marketing",
    "email marketing", "seo", "search engine optimization", "google ranking",
    "website ranking", "google business profile", "google business",
    "google maps", "customer acquisition", "new customers",
    "customer retention", "repeat customers", "customer loyalty",
    "loyal customers", "referral marketing", "referrals", "word of mouth",
    "festival marketing", "seasonal marketing", "local marketing",
    "marketing budget", "marketing roi", "call to action", "cta"
],

"market": [
    "market", "market research", "market analysis", "market validation",
    "market survey", "target customer", "target audience", "customer segment",
    "ideal customer", "customer needs", "customer problem", "pain point",
    "demand", "market demand", "customer demand", "competition", "competitor",
    "competitor analysis", "market gap", "gap in market", "business opportunity",
    "pricing", "pricing strategy", "price research", "location",
    "business location", "shop location", "customer feedback",
    "customer review", "product validation", "business validation", "trend",
    "market trend", "niche", "niche market", "swot", "swot analysis",
    "value proposition", "unique value", "buyer persona", "customer behavior",
    "buying behavior", "market size", "industry", "differentiation",
    "competitive advantage"
],

"communication": [
    "communication", "communication skills", "speaking", "conversation",
    "talking", "confidence", "self confidence", "confidence building",
    "introvert", "shy", "social anxiety", "public speaking", "presentation",
    "speech", "customer handling", "customer interaction", "customer service",
    "difficult customer", "angry customer", "rude customer", "complaint",
    "complaining customer", "bargaining", "price negotiation",
    "active listening", "listening skills", "body language", "eye contact",
    "posture", "hand gestures", "empathy", "understanding customer",
    "persuasion", "convincing customer", "convince", "relationship building",
    "trust", "rapport", "professional communication", "business communication",
    "customer satisfaction", "customer experience", "conflict resolution",
    "argument", "disagreement", "phone communication", "whatsapp communication",
    "email communication", "first impression", "greeting customer",
    "sales communication", "closing a sale"
],

"sales": [
    "sales", "selling", "sell", "sale", "customer psychology",
    "buyer psychology", "buying behavior", "purchase decision", "negotiation",
    "bargaining", "price negotiation", "discount", "offer", "deal",
    "upselling", "cross selling", "repeat customer", "return customer",
    "customer retention", "customer loyalty", "closing sale", "close deal",
    "sales closing", "sales pitch", "pitch", "customer objection",
    "objection handling", "customer doubts", "customer trust",
    "trust building", "value selling", "product value", "pricing", "price",
    "profit", "margin", "follow up", "customer follow up", "sales target",
    "sales goal", "lead", "lead generation", "conversion", "conversion rate",
    "impulse buying", "customer satisfaction", "after sales service",
    "after sales support", "refund", "return policy", "testimonial",
    "customer review", "referral", "word of mouth"
],

"legal": [
    "legal", "law", "business law", "registration", "business registration",
    "register business", "license", "licence", "business license",
    "shop license", "gst", "gst registration", "gst number", "gst return",
    "tax", "taxes", "income tax", "business tax", "udyam", "udyam registration",
    "msme", "msme registration", "government scheme", "government schemes",
    "subsidy", "business subsidy", "loan scheme", "mudra loan",
    "pm mudra yojana", "startup india", "shop act", "shop establishment",
    "shop and establishment act", "trade license", "fssai", "food license",
    "trademark", "brand registration", "copyright", "patent",
    "partnership deed", "partnership agreement", "sole proprietorship",
    "partnership", "llp", "private limited", "compliance", "legal compliance",
    "invoice", "billing", "bill", "pan", "tan", "professional tax",
    "documents", "business documents", "contract", "agreement"
],

"growth": [
    "growth", "business growth", "grow business", "expansion",
    "expand business", "scaling", "scale", "scale up", "reinvestment",
    "reinvest", "reinvest profit", "profit reinvestment", "automation",
    "automate", "business automation", "hiring", "hire employee",
    "recruitment", "employee", "team", "staff", "delegation",
    "delegate work", "second shop", "new branch", "multiple branches",
    "franchise", "business expansion", "product expansion", "new products",
    "new services", "customer growth", "increase customers",
    "increase sales", "sales growth", "productivity", "efficiency",
    "business systems", "standard operating procedure", "sop", "technology",
    "software", "online expansion", "ecommerce", "long term growth",
    "business goals", "growth strategy", "market expansion", "new market",
    "business sustainability", "sustainable growth"
],

"operations": [
    "operations", "business operations", "daily operations", "workflow",
    "daily workflow", "inventory", "stock", "stock management",
    "inventory management", "inventory control", "supplier", "vendor",
    "wholesaler", "manufacturer", "distributor", "backup supplier",
    "procurement", "purchasing", "buying products", "sourcing", "employees",
    "staff", "worker", "recruitment", "hiring", "training", "roles",
    "responsibilities", "quality", "quality control", "quality assurance",
    "packaging", "labeling", "storage", "warehouse", "warehousing",
    "delivery", "shipping", "logistics", "transport", "order",
    "order management", "order processing", "production", "manufacturing",
    "capacity", "equipment", "machines", "tools", "maintenance", "repair",
    "checklist", "standard operating procedure", "sop", "efficiency",
    "productivity", "automation", "expansion"
],

"business": [
    "business", "business idea", "business ideas", "startup", "entrepreneur",
    "entrepreneurship", "product", "product business", "product based",
    "service", "service business", "service based", "online business",
    "offline business", "ecommerce", "manufacturing", "manufacturer",
    "production business", "franchise", "franchise business",
    "business model", "business plan", "value proposition",
    "unique selling proposition", "usp", "problem statement",
    "customer problem", "pain point", "target customer", "target audience",
    "ideal customer", "business opportunity", "market opportunity",
    "business niche", "niche", "business validation", "idea validation",
    "business location", "shop location", "business category", "mission",
    "vision", "competitive advantage", "differentiation", "business goal",
    "business ownership", "sole proprietorship", "partnership",
    "startup cost", "minimum investment", "business success",
    "successful business", "side business", "small business",
    "home business", "business risk"
],

"mindset": [
    "mindset", "business mindset", "entrepreneur mindset", "discipline",
    "consistency", "patience", "long term thinking", "risk", "risk taking",
    "calculated risk", "confidence", "self confidence", "fear",
    "fear of failure", "failure", "motivation", "self motivation",
    "decision making", "decision", "problem solving", "adaptability",
    "flexibility", "learning", "continuous learning", "time management",
    "goal setting", "focus", "stress management", "resilience",
    "mental strength", "growth mindset", "positive thinking",
    "customer first", "leadership", "responsibility", "accountability",
    "self improvement", "habits", "work ethic", "work life balance",
    "perfectionism", "overthinking", "procrastination", "self doubt",
    "persistence", "determination", "vision", "passion", "ego",
    "overconfidence", "humility"
],

"risk": [
    "risk", "business risk", "financial risk", "market risk", "competition",
    "competitor", "backup plan", "emergency", "insurance",
    "business insurance", "covid", "pandemic", "economic crisis",
    "loss prevention", "risk analysis", "risk management",
    "contingency plan", "uncertainty", "failure", "unexpected expenses",
    "business continuity", "disaster recovery"
]

}
