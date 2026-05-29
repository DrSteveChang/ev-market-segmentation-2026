# src/deployment/llm_reporter.py
import os
import logging
import time
from openai import OpenAI
from dotenv import load_dotenv

# Import the structured prompt builder and the strict system persona
from src.deployment.prompt_templates import build_strategic_prompt, SYSTEM_PROMPT

# Load environment variables from the .env file into the system's memory
load_dotenv()

def generate_headless_strategic_insight(model_name: str, metrics: dict, scenario_focus: str):
    """
    Executes a headless LLM call via the Xiaomi MiMo API endpoint.
    Forces structured outputs using a strict system prompt for production-grade reporting.
    Parses both the strategic content and the reasoning trace for statistical auditability.
    """
    logging.info("Triggering Headless LLM Report Generation (Xiaomi MiMo API)...")
    
    # Extract the API key from environment variables
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        logging.warning("MIMO_API_KEY environment variable is missing. Aborting LLM reporting.")
        return None

    # Initialize the OpenAI client targeting the Xiaomi MiMo endpoint
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.xiaomimimo.com/v1"
    )
    
    # Construct the user prompt using the dynamic metrics and scenario focus
    prompt = build_strategic_prompt(scenario_focus, model_name, metrics)

    try:
        # Execute the API call with the specified model and strict system constraints
        response = client.chat.completions.create(
            model="mimo-v2.5-pro", 
            messages=[
                # Inject the rigorous consulting-style system persona
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1 # Maintain low temperature for high determinism and analytical rigor
        )
        
        # Extract the main analytical content
        message_obj = response.choices[0].message
        final_insight = message_obj.content
        
        # Defensively extract the reasoning trace if the model endpoint supports it
        message_dict = message_obj.model_dump()
        reasoning_process = message_dict.get('reasoning_content', 'No automated reasoning trace provided by model endpoint.')
        
        # Define output directory and ensure it exists locally
        output_dir = "data/processed/reports"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate a timestamped filename to prevent overwriting previous executions
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(output_dir, f"Insight_{model_name.replace(' ', '_')}_{timestamp}.md")
        
        # Write the structured output and the audit trail to a local Markdown file
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# Automated Strategic Insight: {model_name}\n\n")
            f.write("## Executive Summary\n")
            f.write(f"{final_insight}\n\n")
            f.write("---\n## Audit Trail (LLM Reasoning Trace)\n")
            f.write(f"> {reasoning_process}\n")
            
        logging.info(f"Strategic insight report successfully saved to: {report_path}")
        return final_insight

    except Exception as e:
        # Log the exact error for debugging purposes if the API call drops
        logging.error(f"Xiaomi MiMo API execution failed: {e}")
        return None