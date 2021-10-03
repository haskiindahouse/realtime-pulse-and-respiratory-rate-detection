def plainTextStyle():
    return """
QPlainTextEdit
{
background-color: #b1b1b1;
color: #202020;
border: 1px solid #031582;
selection-background-color: #505050;
selection-color: #ACDED5;
}
QMenu
{
background: #F2F2F2;
color: #0E185F;
border: 1px solid #000;
selection-background-color: #ACDED5;

} 
    """


def pushButtonStyle():
    return """
    QPushButton
{
    color: #000000;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-width: 1px;
    border-color: #1e1e1e;
    border-style: solid;
    border-radius: 6;
    padding: 3px;
    font-size: 12px;
    padding-left: 5px;
    padding-right: 5px;
}
QPushButton:pressed
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
}
    """


def mainWindowStyle():
    return """
    QWidget {
  background-color: black;
}
"""

def lineEditStyle():
    return """
    QLineEdit {
    background-color: white;
    }
    """