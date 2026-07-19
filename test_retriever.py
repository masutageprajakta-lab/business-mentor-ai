from retriever import retrieve_card

tests = [
    "What is ROI?",
    "Explain working capital",
    "What is break even point?",
    "What is cost price?",
    "What is selling price?",
    "What is investment?"
]

for q in tests:
    topic, card = retrieve_card("finance", q)

    print("--------------------------------")
    print("Question :", q)
    print("Matched  :", topic)

    if card:
        print("Definition:", card["definition"])