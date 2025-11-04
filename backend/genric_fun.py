import re

def extract_session_id(session_str: str):
    match = re.findall(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        return match[0]  # return the first (and only) match
    return ""

def get_str_resp_from_fooddict(food_dict:dict):
    return ", ".join([f"{int(value)} {key}" for key ,value in food_dict.items()])

if __name__ == "__main__":
    print(extract_session_id(
        "projects/aadi-pgpf/agent/sessions/e9cf1090-4ea1-9e5a-3e21-398e2a696ff8/contexts/ongoing-order"
    ))

