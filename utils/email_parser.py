from email import message_from_string
from email.parser import Parser
from email.policy import default

def parse_email_content(raw_email_string):
    """
    Parsea una cadena de correo cruda (RFC822) y extrae sus componentes principales
    
    Args:
        raw_email_string (str): El correo en formato RFC822
        
    Returns:
        dict: Diccionario con los campos parsed del correo
    """
    # Parsear el correo
    email_message = message_from_string(raw_email_string, policy=default)
    
    # Extraer información básica
    parsed_data = {
        'subject': email_message.get('Subject', ''),
        'from': email_message.get('From', ''),
        'to': email_message.get('To', ''),
        'date': email_message.get('Date', ''),
        'body': '',
        'attachments': []
    }
    
    # Procesar el cuerpo del mensaje
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                parsed_data['body'] = part.get_payload(decode=True).decode()
                break
            elif part.get_content_maintype() != 'multipart':
                # Guardar información de adjuntos
                filename = part.get_filename()
                if filename:
                    parsed_data['attachments'].append({
                        'filename': filename,
                        'content_type': part.get_content_type()
                    })
    else:
        parsed_data['body'] = email_message.get_payload(decode=True).decode()
    
    return parsed_data

def format_email_for_display(parsed_email_dict):
    """
    Formatea un correo parseado para mostrarlo de manera legible y atractiva en consola
    
    Args:
        parsed_email_dict (dict): Diccionario con la información del correo
        
    Returns:
        str: Representación formateada del correo
    """
    # Encabezado visual destacado
    template = f"""
{'='*60}
📧  CORREO ELECTRÓNICO
{'='*60}
De:      {parsed_email_dict['from']}
Para:    {parsed_email_dict['to']}
Fecha:   {parsed_email_dict['date']}
Asunto:  {parsed_email_dict['subject']}
{'-'*60}
{parsed_email_dict['body']}
{'-'*60}"""
    
    if parsed_email_dict['attachments']:
        template += "\nArchivos adjuntos:\n"
        for attachment in parsed_email_dict['attachments']:
            template += f"- {attachment['filename']} ({attachment['content_type']})\n"
    template += f"{'='*60}\n"
    
    return template
