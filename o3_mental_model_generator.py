# mental_model_generator.py

import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------
# Step 1: Define Prompt
# -------------------------
def build_prompt(topic):
    return f"""
You are a concept architect. Given a topic, generate a mental model that includes:
- A core definition
- Key subtopics or dimensions
- Sub-components under each subtopic (up to 2 levels)
- Logical or causal relationships (if applicable)

Output format:
1. JSON tree showing core idea, subtopics, and children.
2. Markdown-based diagram of the same structure.

Topic: {topic}
"""

# -------------------------
# Step 2: Call OpenAI o3 Model (Response API style)
# -------------------------
def generate_mental_model(topic):
    prompt = build_prompt(topic)

    response = openai.chat.completions.create(
        model="gpt-4o",  # Use o3 if available under 'gpt-4o' or use o3 directly via Response API
        messages=[
            {"role": "system", "content": "You are a helpful assistant for mental model generation."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

# -------------------------
# Step 3: Optional Output Parsing
# -------------------------
def parse_mental_model_output(response_text):
    try:
        parts = response_text.split("```")
        parsed = {"json": "", "markdown": ""}
        for part in parts:
            if part.strip().startswith("json"):
                parsed["json"] = json.loads(part.strip().split("\n", 1)[1])
            elif not part.startswith("json") and part.strip().startswith("-"):
                parsed["markdown"] = part.strip()
        return parsed
    except Exception as e:
        print("Warning: Could not parse structured response. Returning raw.")
        return {"raw": response_text}

# -------------------------
# Step 4: Entry Point
# -------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a mental model for a given topic.")
    parser.add_argument("topic", type=str, help="Topic to generate mental model for")
    args = parser.parse_args()

    print(f"\n🧠 Generating mental model for: {args.topic}\n")
    output = generate_mental_model(args.topic)
    print("\n📤 Raw Response:\n")
    print(output)

    parsed = parse_mental_model_output(output)

    if "json" in parsed:
        with open("mental_model.json", "w") as f:
            json.dump(parsed["json"], f, indent=2)
        print("\n✅ Saved structured model to mental_model.json")

    if "markdown" in parsed:
        with open("mental_model_diagram.md", "w") as f:
            f.write(parsed["markdown"])
        print("✅ Saved diagram to mental_model_diagram.md")

    if "raw" in parsed:
        with open("mental_model_raw.md", "w") as f:
            f.write(parsed["raw"])
        print("✅ Saved fallback raw output to mental_model_raw.md")
