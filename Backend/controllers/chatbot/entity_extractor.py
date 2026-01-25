"""
Entity Extractor - Extracts structured data from AI responses
"""
import re
import json

def extract_json_from_llm(text):
    """
    Extract and parse JSON from LLM response (handles markdown fences, incomplete JSON)
    
    Args:
        text (str): Raw AI response that may contain JSON
    
    Returns:
        dict: Parsed JSON object, or empty dict if parsing fails
    """
    try:
        if not text or not text.strip():
            print("[JSON EXTRACTION ERROR] Empty response from AI")
            return {}
        
        # Remove markdown code fences
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"```(?:json)?\s*", "", cleaned)
            cleaned = cleaned.replace("```", "")
        
        # Fix common malformed JSON patterns
        # Fix "entities:{}" -> "entities":{}
        cleaned = re.sub(r'"entities:\{', '"entities":{', cleaned)
        # Fix missing quotes around keys
        cleaned = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', cleaned)
        
        # Fix incomplete JSON - count braces and add missing ones
        open_braces = cleaned.count('{')
        close_braces = cleaned.count('}')
        if open_braces > close_braces:
            cleaned = cleaned + ('}' * (open_braces - close_braces))
        
        # Try to parse the entire cleaned text first
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass
        
        # Find the first { and try to parse from there
        first_brace = cleaned.find('{')
        if first_brace != -1:
            json_candidate = cleaned[first_brace:]
            # Fix braces again after slicing
            open_braces = json_candidate.count('{')
            close_braces = json_candidate.count('}')
            if open_braces > close_braces:
                json_candidate = json_candidate + ('}' * (open_braces - close_braces))
            
            try:
                return json.loads(json_candidate)
            except json.JSONDecodeError:
                pass
        
        # Fallback: use regex to extract nested JSON
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
        
        print(f"[JSON EXTRACTION ERROR] Could not parse JSON from AI response")
        print(f"[FULL RESPONSE] {text}")
        return {}
    
    except json.JSONDecodeError as e:
        print(f"[JSON PARSE ERROR] {str(e)}")
        print(f"[FAILED TEXT] {text}")
        return {}
    except Exception as e:
        print(f"[EXTRACTION ERROR] {str(e)}")
        return {}
