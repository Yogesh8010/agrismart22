import pickle

# Basic dictionary-based chatbot
faq_data = {
    "what fertilizer to use for wheat": "Use Urea or DAP for wheat crops.",
    "how to control pests naturally": "Use neem oil, soap sprays, and crop rotation.",
    "how to improve soil ph": "Use lime for acidic soil or sulfur for alkaline soil.",
    "how to increase crop yield": "Ensure timely irrigation, use certified seeds and proper fertilization.",
    "what is best pesticide for vegetables": "Try neem-based organic pesticides or pyrethrin.",
    "how to protect crops from insects": "Use insect nets, pest-repellent plants, and field monitoring.",
    "how to treat fungal infection in crops": "Use copper-based fungicides or rotate crops regularly.",
    "what should be ideal soil ph for crops": "Most crops grow best in a pH range of 6.0 to 7.5."
}

# Save as chatbot model
with open('chatbot_model.pkl', 'wb') as f:
    pickle.dump(faq_data, f)

print("✅ Chatbot model saved as chatbot_model.pkl")
