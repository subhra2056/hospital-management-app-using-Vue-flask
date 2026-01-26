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
        # Try to find the outermost braces
        start = cleaned.find('{')
        end = cleaned.rfind('}')
        
        # If no closing brace found, the JSON might be incomplete - try to find where it should end
        if start != -1 and end == -1:
            # JSON starts but doesn't close - try to add closing braces
            open_count = cleaned[start:].count('{')
            close_count = cleaned[start:].count('}')
            if open_count > close_count:
                # Add missing closing braces
                cleaned = cleaned + '}' * (open_count - close_count)
                end = len(cleaned) - 1
        
        if start != -1 and end != -1 and end > start:
            json_candidate = cleaned[start:end+1]
            try:
                return json.loads(json_candidate)
            except json.JSONDecodeError as e:
                # If first attempt fails, try to repair common issues
                try:
                    # Fix missing quotes around keys: {key: "value"} -> {"key": "value"}
                    fixed_candidate = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_candidate)
                    
                    # Count braces and brackets to check for missing closing characters
                    open_braces = fixed_candidate.count('{')
                    close_braces = fixed_candidate.count('}')
                    open_brackets = fixed_candidate.count('[')
                    close_brackets = fixed_candidate.count(']')
                    
                    # Add missing closing braces/brackets
                    if open_braces > close_braces:
                        fixed_candidate += '}' * (open_braces - close_braces)
                    if open_brackets > close_brackets:
                        fixed_candidate += ']' * (open_brackets - close_brackets)
                    
                    # Fix malformed empty objects: {"entities":{"}} -> {"entities":{}}
                    # Handle cases where there's a stray quote or extra brace in empty objects
                    fixed_candidate = re.sub(r'"entities"\s*:\s*\{\s*"\s*\}\s*\}', '"entities": {}}', fixed_candidate)
                    fixed_candidate = re.sub(r'"entities"\s*:\s*\{\s*\}\s*\}', '"entities": {}}', fixed_candidate)
                    
                    # Fix empty objects with stray quotes: {"key":{""}} -> {"key":{}}
                    fixed_candidate = re.sub(r':\s*\{\s*"\s*"\s*\}', ': {}', fixed_candidate)
                    
                    # Fix trailing commas before closing braces/brackets
                    fixed_candidate = re.sub(r',\s*}', '}', fixed_candidate)
                    fixed_candidate = re.sub(r',\s*]', ']', fixed_candidate)
                    
                    # Try parsing again
                    return json.loads(fixed_candidate)
                except Exception as repair_error:
                    # If repair failed, try one more time with just adding missing braces
                    try:
                        open_braces = json_candidate.count('{')
                        close_braces = json_candidate.count('}')
                        open_brackets = json_candidate.count('[')
                        close_brackets = json_candidate.count(']')
                        
                        simple_fix = json_candidate
                        if open_braces > close_braces:
                            simple_fix += '}' * (open_braces - close_braces)
                        if open_brackets > close_brackets:
                            simple_fix += ']' * (open_brackets - close_brackets)
                        
                        return json.loads(simple_fix)
                    except:
                        print(f"[JSON REPAIR FAILED] {str(repair_error)}")
                        print(f"[ORIGINAL] {json_candidate}")
                        pass
                
        # Regex to match valid JSON entries more robustly
        # This regex matches { "key": ... } patterns
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if match:
             try:
                return json.loads(match.group(0))
             except:
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
