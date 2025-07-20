import re
import json

def parse_textmap(file_path):
    """
    Parses a TEXTMAP file and extracts map data using a state-based approach.
    Assigns sequential IDs as they appear in the file.
    """
    map_data = {
        "vertices": [],
        "linedefs": [],
        "sidedefs": [],
        "sectors": [],
        "things": []
    }

    # Definir estados do parser
    STATE_OUTSIDE_BLOCK = 0
    STATE_EXPECTING_OPEN_BRACE = 1
    STATE_INSIDE_BLOCK = 2

    current_state = STATE_OUTSIDE_BLOCK
    current_block_type = None
    current_block_entry = None
    
    # Mapeamento do tipo de bloco
    block_type_to_key = {
        "vertex": "vertices",
        "linedef": "linedefs",
        "sidedef": "sidedefs",
        "sector": "sectors",
        "thing": "things"
    }

    # Padrões regex
    block_name_pattern = re.compile(r'^\s*(vertex|linedef|sidedef|sector|thing)\s*$', re.IGNORECASE)
    open_brace_pattern = re.compile(r'^\s*{\s*$')
    block_end_pattern = re.compile(r'^\s*}\s*$')
    attribute_pattern = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*?)\s*;$')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                original_line = line.rstrip('\r\n')
                line_stripped = original_line.strip()

                # Ignorar linhas vazias e comentários
                if not line_stripped or line_stripped.startswith("//"):
                    continue

                if current_state == STATE_OUTSIDE_BLOCK:
                    match_block = block_name_pattern.match(line_stripped)
                    if match_block:
                        current_block_type = match_block.group(1).lower()
                        current_state = STATE_EXPECTING_OPEN_BRACE

                elif current_state == STATE_EXPECTING_OPEN_BRACE:
                    if open_brace_pattern.match(line_stripped):
                        if current_block_type in block_type_to_key:
                            new_entry = {"id": len(map_data[block_type_to_key[current_block_type]])}
                            map_data[block_type_to_key[current_block_type]].append(new_entry)
                            current_block_entry = new_entry
                            current_state = STATE_INSIDE_BLOCK
                        else:
                            print(f"ERRO[{line_num}]: Tipo de bloco '{current_block_type}' não reconhecido")
                            current_state = STATE_OUTSIDE_BLOCK
                    else:
                        print(f"ERRO[{line_num}]: Esperava '{{' após '{current_block_type}'")
                        current_state = STATE_OUTSIDE_BLOCK

                elif current_state == STATE_INSIDE_BLOCK:
                    if block_end_pattern.match(line_stripped):
                        current_state = STATE_OUTSIDE_BLOCK
                    else:
                        match_attr = attribute_pattern.match(original_line)
                        if match_attr:
                            attr_name = match_attr.group(1).lower()
                            attr_value_str = match_attr.group(2).strip()
                            
                            try:
                                if '.' in attr_value_str:
                                    attr_value = float(attr_value_str)
                                elif attr_value_str.lower() in ['true', 'false']:
                                    attr_value = attr_value_str.lower() == 'true'
                                else:
                                    attr_value = int(attr_value_str)
                            except ValueError:
                                attr_value = attr_value_str
                            
                            current_block_entry[attr_name] = attr_value

    except UnicodeDecodeError:
        print(f"ERRO: Falha ao ler arquivo como UTF-8: {file_path}")
        return None
    except Exception as e:
        print(f"ERRO inesperado: {str(e)}")
        return None

    return map_data

# Exemplo de uso
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "TEXTMAP.txt"

    print(f"Processando arquivo: {input_file}")
    result = parse_textmap(input_file)
    
    if result:
        print("\nResultado da análise:")
        print(f"- Vértices: {len(result['vertices'])}")
        print(f"- Linedefs: {len(result['linedefs'])}")
        print(f"- Sidedefs: {len(result['sidedefs'])}")
        print(f"- Setores: {len(result['sectors'])}")
        print(f"- Things: {len(result['things'])}")
        
        output_file = "parsed_map.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"\nDados salvos em: {output_file}")
    else:
        print("Falha ao processar o arquivo.")