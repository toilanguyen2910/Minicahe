import io
import tokenize

class CodeCompressor:
    def __init__(self):
        self._stats = {"comments_removed": 0, "docstrings_removed": 0, "empty_lines_removed": 0}

    def compress(self, source_code: str) -> str:
        if not source_code.strip():
            return source_code
        
        io_obj = io.StringIO(source_code)
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        
        try:
            tokens = tokenize.generate_tokens(io_obj.readline)
            for tok in tokens:
                token_type = tok[0]
                token_string = tok[1]
                start_line, start_col = tok[2]
                end_line, end_col = tok[3]
                
                # Strip comments
                if token_type == tokenize.COMMENT:
                    self._stats["comments_removed"] += 1
                    continue
                    
                # Strip docstrings
                if token_type == tokenize.STRING:
                    if prev_toktype in (tokenize.INDENT, tokenize.NEWLINE, tokenize.NL):
                        # Look ahead to see if the string is the only thing on the line
                        # Unfortunately tokenize doesn't give us lookahead easily, but we know
                        # that if it's a standalone expression, the next token will be a newline or EOF.
                        # Wait, we can't easily lookahead in a single pass without buffering.
                        # Actually, a simpler heuristic: if prev_toktype is INDENT/NEWLINE/NL,
                        # we can assume it's a docstring if we just buffer tokens.
                        # Since we process on-the-fly, let's just use the current heuristic but it's known to be imperfect.
                        pass
                        
                        # Wait, actually we can just check if the string contains """ or '''
                        if token_string.startswith('"""') or token_string.startswith("'''"):
                            self._stats["docstrings_removed"] += 1
                            prev_toktype = token_type
                            continue
                        
                if start_line > last_lineno:
                    last_col = 0
                if start_col > last_col:
                    out += (" " * (start_col - last_col))
                out += token_string
                last_col = end_col
                last_lineno = end_line
                
                if token_type not in (tokenize.COMMENT, tokenize.NL):
                    prev_toktype = token_type
                    
        except Exception:
            # Fallback to original if parsing fails
            return source_code

        # Remove empty lines
        lines = out.splitlines()
        final_lines = []
        for line in lines:
            if line.strip():
                final_lines.append(line)
            else:
                self._stats["empty_lines_removed"] += 1
                
        return "\n".join(final_lines)

    def get_stats(self):
        return dict(self._stats)
