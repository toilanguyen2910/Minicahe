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
