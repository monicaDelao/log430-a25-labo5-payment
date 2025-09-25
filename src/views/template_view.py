"""
Template view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

def show_404_page():
    """ Show 404 page """
    return get_template("<h2>404 Page Not Found</h2><p>Desolé, la page que vous recherchez semble introuvable.<p>")

def xml_to_dict(element):
    """Convert XML element to dictionary"""
    result = {}
    
    # If element has text content and no children, use the text
    if element.text and not list(element):
        return element.text.strip()
    
    # Process child elements
    for child in element:
        child_data = xml_to_dict(child)
        
        # Handle multiple elements with same tag (convert to list)
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
    
    return result

def get_param(params, name):
    """Get and sanitize parameters from XML request"""
    if not params or not name:
        return ""
    
    # Navigate nested dictionary structure if needed
    value = params.get(name)
    
    if value is None:
        return ""
    
    # If it's a list (multiple elements with same name), get first one
    if isinstance(value, list):
        return str(value[0]) if value else ""
    
    # Convert to string and return
    return str(value)

def get_template(content):
    """ Inject content into base HTML template for the application """
    breadcrumb_text = """<p>Application de gestion de paiements</p>"""
    return f"""<!DOCTYPE html>
    <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
            <link rel="stylesheet" href="/assets/light.css">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <header>
                <h1>PaymentServiceSOA</h1>
            </header>
            <div id="breadcrumbs">
                {breadcrumb_text}
            </div>
            <hr>
            {content}
        </body>
    </html>
    """