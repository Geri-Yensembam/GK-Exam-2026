from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

def generate_admit_card(student):
    from io import BytesIO
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # White background
    p.setFillColor(colors.white)
    p.rect(0, 0, width, height, fill=1, stroke=0)

    # Header background
    p.setFillColor(colors.HexColor('#1a2740'))
    p.rect(0, height - 130, width, 130, fill=1, stroke=0)

    # Header text
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 25)
    p.drawCentredString(width/2, height - 50, "CHEKLA COLLEGE OF ENGINEERING")
    p.setFont("Helvetica", 16)
    p.drawCentredString(width/2, height - 75, "GK Exam 2026")
    p.setFont("Helvetica-Bold", 13)
    p.setFillColor(colors.HexColor('#4fc3f7'))
    p.drawCentredString(width/2, height - 100, "ADMIT CARD")

    # Blue accent line
    p.setFillColor(colors.HexColor('#4fc3f7'))
    p.rect(0, height - 133, width, 3, fill=1, stroke=0)

    # Card white body
    p.setFillColor(colors.HexColor('#f5f6fa'))
    p.rect(30, height - 600, width - 60, 450, fill=1, stroke=0)

    # Roll number box - positioned properly below header
    p.setFillColor(colors.HexColor('#1a2740'))
    p.roundRect(width - 170, height - 200, 130, 55, 8, fill=1, stroke=0)
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 8)
    p.drawCentredString(width - 105, height - 163, "ROLL NUMBER")
    p.setFont("Helvetica-Bold", 18)
    roll = student.roll_number if student.roll_number else "TBA"
    p.drawCentredString(width - 105, height - 185, roll)

    # Student Details heading
    p.setFillColor(colors.HexColor('#1a2740'))
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 165, "Student Details")

    # Divider line
    p.setStrokeColor(colors.HexColor('#4fc3f7'))
    p.setLineWidth(2)
    p.line(50, height - 172, width - 220, height - 172)

    # Student details
    details = [
        ("Name", student.full_name),
        ("Email", student.email),
        ("Phone", student.phone),
        ("College", student.college),
        ("Department", student.department),
        ("Year of Study", student.year_of_study),
        ("Gender", student.gender),
        ("Subject", student.subject),
    ]

    y = height - 200
    for label, value in details:
        # Label box
        p.setFillColor(colors.HexColor('#1a2740'))
        p.setFont("Helvetica-Bold", 9)
        p.drawString(50, y, label.upper())
        # Value
        p.setFillColor(colors.HexColor('#2c3e50'))
        p.setFont("Helvetica", 11)
        p.drawString(200, y, str(value))
        # Subtle line
        p.setStrokeColor(colors.HexColor('#e0e0e0'))
        p.setLineWidth(0.5)
        p.line(50, y - 8, width - 50, y - 8)
        y -= 30

    # Exam info box
    p.setFillColor(colors.HexColor('#1a2740'))
    p.roundRect(30, height - 580, width - 60, 60, 8, fill=1, stroke=0)
    p.setFillColor(colors.HexColor('#4fc3f7'))
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(width/2, height - 545, "EXAMINATION DETAILS")
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, height - 563, 
        "Date: 15th June 2026   |   Center: Chekla College of Engineering, Pune   |   Time: 10:00 AM")

    # Footer
    p.setFillColor(colors.HexColor('#1a2740'))
    p.rect(0, 0, width, 45, fill=1, stroke=0)
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 9)
    p.drawCentredString(width/2, 25, 
        "Computer generated admit card | GK Exam 2026 | Chekla College of Engineering, Pune")
    p.setFont("Helvetica", 8)
    p.setFillColor(colors.HexColor('#4fc3f7'))
    p.drawCentredString(width/2, 10, 
        "Bring this admit card + valid photo ID to the examination center")

    p.save()
    buffer.seek(0)
    return buffer