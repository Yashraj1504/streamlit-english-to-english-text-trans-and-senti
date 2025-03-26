









import streamlit as st
import json
from langchain_groq import ChatGroq

# Initialize ChatGroq model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="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"  # Replace with your actual API key
)

def classify_speakers(conversation_text):
    messages = [
        (
            "system",
            "You are an AI that classifies speakers in a conversation as either 'Client' or 'Agent'.\n"
            "A Client asks for information or makes requests, while an Agent provides answers or handles requests.\n"
            "Additionally, provide:\n"
            "- An **Agent rating** out of 10 based on professionalism, clarity, and engagement.\n"
            "- An **analysis breakdown** of the Agent's behavior for each sentence.\n"
            "- The **factors used for rating** (such as politeness, accuracy, efficiency, etc.).\n\n"
            "- A detailed **Agent behavior breakdown**, mapping each client statement to the respective agent response and its evaluation.\n"
            "### Important Instructions:\n"
            "1. **Return the output strictly in valid JSON format**.\n"
            "2. **Do NOT add extra text, explanations, or markdown**.\n"
            "3. **Ensure this exact JSON structure**:\n"
            "{\n"
            '  "classification": {"agent": "Speaker A", "client": "Speaker B"},\n'
            '  "rating": 8,\n'
            '  "analysis": [\n'
            '    {"category": "Introduction", "description": "Professional greeting"},\n'
            '    {"category": "Verification", "description": "Clear and concise"}\n'
            '  ],\n'
            '  "rating_factors": ["Professionalism", "Clarity", "Politeness"]\n'
            '  "agent_behavior": [\n'
            '    {"client_statement": "Client: I need help with my account.",\n'
            '     "agent_response": "Agent: Sure, I can assist you. What issue are you facing?",\n'
            '     "evaluation": "Helpful and professional"}\n'
            '  ]\n'
            "}"
        ),
        (
            "human",
            conversation_text
        ),
    ]
    
    ai_msg = llm.invoke(messages)

    try:
        # Extract only JSON part from response
        json_start = ai_msg.content.find("{")
        json_end = ai_msg.content.rfind("}") + 1
        json_text = ai_msg.content[json_start:json_end].strip()

        # Load the extracted JSON
        structured_response = json.loads(json_text)
    except json.JSONDecodeError:
        structured_response = {"error": "AI response was not in valid JSON format. Please try again."}
    
    return structured_response

# Streamlit UI
st.title("🔹 Client-Agent Text Classification")
st.write("Enter the conversation text below and click 'Classify' to get the AI analysis.")

# Text input area
conversation_text = st.text_area("✍️ Enter conversation text:")

# Show input text in the output section as well
st.write("### 📥 Your Input:")
st.write(f"```{conversation_text}```")  # Display as a code block

if st.button("🚀 Classify"):
    if conversation_text.strip():
        result = classify_speakers(conversation_text)
        
        if "error" in result:
            st.error(result["error"])
        else:
            st.subheader("✅ Classification Result")
            st.write(f"🔹 **Agent:** {result['classification']['agent']}")
            st.write(f"🔹 **Client:** {result['classification']['client']}")
            st.write(f"⭐ **Agent Rating:** {result['rating']}/10")
            
            st.subheader("📊 Analysis Breakdown")
            for item in result["analysis"]:
                st.write(f"- **{item['category']}**: {item['description']}")
            
            st.subheader("📌 Rating Factors")
            for factor in result["rating_factors"]:
                st.write(f"- {factor}")

            st.subheader("🔍 Agent Behavior on Each Statement")
            for item in result["agent_behavior"]:
                st.write(f"- **Client:** {item['client_statement']}")
                st.write(f"  **Agent:** {item['agent_response']}")
                st.write(f"  🏷 **Evaluation:** {item['evaluation']}")
                st.write("---")  # Adds a separator

    else:
        st.warning("⚠️ Please enter conversation text before classifying.")
