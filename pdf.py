from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_test_pdf(filename, title, content):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, title)
    
    # Body Content
    c.setFont("Helvetica", 12)
    text_object = c.beginText(72, height - 100)
    text_object.setLeading(14)
    
    # Wrap text manually for the PDF
    lines = content.split('\n')
    for line in lines:
        text_object.textLine(line)
        
    c.drawText(text_object)
    c.save()
    print(f"[✓] Created: {filename}")

# --- PDF 1: Healthcare & AI ---
content_1 = """
Artificial Intelligence is transforming modern healthcare through 
advanced diagnostics and personalized medicine. Machine learning 
algorithms can analyze medical imagery with higher precision than 
human doctors in some cases. By processing vast amounts of patient 
data, AI helps in early detection of chronic diseases like cancer 
and heart conditions. Robotic surgery and virtual nursing assistants 
are also becoming common in smart hospitals.
"""

# --- PDF 2: Space Exploration ---
content_2 = """
The exploration of Mars has become a primary goal for space agencies 
worldwide. NASA's Perseverance rover is currently searching for 
signs of ancient microbial life in the Jezero Crater. Future 
manned missions to the Red Planet require significant advances in 
propulsion technology and life support systems. SpaceX and other 
private companies are developing the Starship rocket to make 
interplanetary travel more sustainable and frequent.
"""

if __name__ == "__main__":
    create_test_pdf("example_1.pdf", "AI in Modern Healthcare", content_1)
    create_test_pdf("example_2.pdf", "The Future of Mars Exploration", content_2)