import re
import sys

class LiterallyEveryLang:
    def __init__(self):
        self.assets = {}  # Our "Stakeholder" variables
        self.is_terminated = False
        
    def log_error(self, message):
        print(f"[E] LITIGATION_ERROR: {message}")
        print("    ACTION: Liquidating assets and filing for Chapter 11.")
        sys.exit(1)

    def evaluate_math(self, expression):
        """Processes 'Calculate Sales' logic with JS-style loose typing."""
        # Replace 'cs' with actual Python operators for evaluation
        # We'll support basic patterns like '5 cs 10'
        try:
            # Handle the 'cs' keyword by replacing it with '+' (the ultimate sales multiplier)
            # or more complex logic if needed. For now, it acts as a generic operator.
            clean_expr = expression.replace('cs', '+').strip()
            return eval(clean_expr, {}, self.assets)
        except Exception as e:
            return f"{expression}_SYNERGY_BLOB"

    def run(self, code):
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            
            if self.is_terminated:
                break

            # 1. CC THE BOARD (print)
            if line.startswith("cctb"):
                content = line[4:].strip()
                # Check if it's a known asset or a raw string
                output = self.assets.get(content, content.strip('"').strip("'"))
                print(f"[BOARD_MEMO]: {output}")

            # 2. INCENTIVISE (variable declaration)
            # Syntax: inc asset_name = value
            elif line.startswith("inc"):
                match = re.match(r"inc\s+(\w+)\s*=\s*(.*)", line)
                if match:
                    name, value_expr = match.groups()
                    # If math is involved via 'cs'
                    if 'cs' in value_expr:
                        self.assets[name] = self.evaluate_math(value_expr)
                    else:
                        # Simple assignment
                        try:
                            self.assets[name] = eval(value_expr, {}, self.assets)
                        except:
                            self.assets[name] = value_expr.strip('"').strip("'")
                else:
                    self.log_error(f"Malformed Incentive Structure on line {i+1}")

            # 3. PIVOT ON KPI (if/else)
            # Simplified syntax: pok (asset) { code }
            elif line.startswith("pok"):
                match = re.search(r"pok\s*\((.*)\)\s*\{(.*)\}", line)
                if match:
                    condition_expr, branch = match.groups()
                    # Evaluate condition
                    if eval(condition_expr, {}, self.assets):
                        self.run(branch)
                else:
                    # Check for multi-line block or simple one-liner
                    pass

            # 4. LIGHT THE BUILDING ON FIRE (end)
            elif line == "ltbof":
                print("[!] Building is on fire. Corporate insurance claimed. We are out.")
                self.is_terminated = True
                break

            # Catch-all for unrecognized buzzwords
            else:
                if line:
                    print(f"[?] Unrecognized Buzzword: '{line}'. The Intern is confused.")

# Example Usage of the Business Logic
if __name__ == "__main__":
    business_logic = """
    // Initialize the Q4 Budget
    inc budget = 50
    inc marketing_spend = 50000 cs 25000
    
    cctb "Total Marketing Liquidity:"
    cctb marketing_spend
    
    // Check if we can afford a pizza party
    pok (budget > 10000) { cctb "Order 1 Large Pepperoni for 500 employees." }
    
    ltbof
    """
    
    interpreter = LiterallyEveryLang()
    print("--- STARTING CORPORATE SPRINT ---\n")
    interpreter.run(business_logic)
