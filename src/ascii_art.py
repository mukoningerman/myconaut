"""
Myconaut - ASCII Art Assets
"""

from config import Config
from colorama import Style

class ASCIIArt:
    """Collection of ASCII art for the game"""

    @staticmethod
    def title_screen():
        """Main title screen"""
        return f"""
{Config.COLORS['title']}
╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║  ███╗   ███╗██╗   ██╗ ██████╗ ██████╗ ███╗   ██╗ █████╗ ██╗   ██╗████████╗  ║
║  ████╗ ████║╚██╗ ██╔╝██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║   ██║╚══██╔══╝  ║
║  ██╔████╔██║ ╚████╔╝ ██║     ██║   ██║██╔██╗ ██║███████║██║   ██║   ██║     ║
║  ██║╚██╔╝██║  ╚██╔╝  ██║     ██║   ██║██║╚██╗██║██╔══██║██║   ██║   ██║     ║
║  ██║ ╚═╝ ██║   ██║   ╚██████╗╚██████╔╝██║ ╚████║██║  ██║╚██████╔╝   ██║     ║
║  ╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝    ╚═╝     ║
║                                                                             ║
║                                                                             ║
║                       A Psychedelic Fungal Adventure                        ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
{Config.COLORS['highlight']}
                            Version {Config.VERSION}
                            By {Config.AUTHOR}
{Config.COLORS['normal']}
"""

    @staticmethod
    def forest():
        """Forest location art"""
        return r"""
          ^^^              ^^^
         ^^^^^            ^^^^^
        ^^^^^^^          ^^^^^^^
          |||              |||
          |||              |||
         \|||/            \|||/
          \|/              \|/
           |                |
""" + f"""
{Config.COLORS['mushroom']}
           ()               ()
          (  )             (  )
         (    )           (    )
        (      )         (      )
{Config.COLORS['normal']}
    You are in the Whispering Forest...
"""

    @staticmethod
    def cave():
        """Cave location art"""
        return r"""
        ___________________________
       /                           \
      /        _____________        \
     /        /             \        \
    /        /               \        \
   /        /                 \        \
  /________/                   \________\
  |                                      |
  |                                      |
  |          Dark Fungal Caverns         |
  |______________________________________|
""" + f"""
{Config.COLORS['normal']}
"""

    @staticmethod
    def village():
        """Village location art"""
        return r"""
          /\                  /\
         /  \                /  \
        /____\              /____\
         |  |                |  |
         |  |                |  |
        _|__|_              _|__|_
""" + f"""
{Config.COLORS['normal']}
    Welcome to Myconid Village...
"""

    @staticmethod
    def swamp():
        """Swamp location art"""
        return r"""
      ~~  ~      ~  ~~
    ~    oOo   oOo    ~
   ~    O   O O   O    ~
  ~~~    oOo   oOo    ~~~
     ~~~          ~~~
        ~~~~~~~~~~
""" + f"""
{Config.COLORS['mushroom']}
        ()   ()   ()
       (  ) (  ) (  )
      (    )    (    )
{Config.COLORS['normal']}
    The Murky Swamp bubbles with life...
"""

    @staticmethod
    def mountain():
        """Mountain location art"""
        return r"""
              /\
             /  \
            /    \
           /      \
          /        \
         /          \
        /            \
       /______________\
""" + f"""
{Config.COLORS['normal']}
    The Crystal Peak mountains...
"""

    @staticmethod
    def player():
        """Player character art"""
        return r"""
       ╔══════════╗
       ║    ☺     ║
       ║   /|\    ║
       ║   / \    ║
       ╚══════════╝
""" + f"""
{Config.COLORS['normal']}
"""

    @staticmethod
    def enemy_sporefang():
        """Sporefang enemy art"""
        return r"""
        ╔════════════╗
        ║   (•_•)    ║
        ║   /| |\    ║
        ║    | |     ║
        ║   ╰╦ ╦╯    ║
        ╚════════════╝
""" + f"""
{Config.COLORS['normal']}
"""

    @staticmethod
    def enemy_thornbeast():
        """Thornbeast enemy art"""
        return r"""
        ╔══════════════╗
        ║     ^ ^      ║
        ║    (•▼•)     ║
        ║    /| |\     ║
        ║   ╰╦╦ ╦╦╯    ║
        ╚══════════════╝
""" + f"""
{Config.COLORS['normal']}
"""

    @staticmethod
    def elder_myconid():
        """Elder Myconid NPC art"""
        return r"""
         ╔════════════╗
         ║   (^_^)    ║
         ║   /|||\    ║
         ║   ╰────╯   ║
         ╚════════════╝
""" + f"""
{Config.COLORS['normal']}
"""

    @staticmethod
    def border_horizontal(width=80):
        """Horizontal border"""
        return "═" * width

    @staticmethod
    def border_vertical():
        """Vertical border"""
        return "║"

    @staticmethod
    def corner_top_left():
        return "╔"

    @staticmethod
    def corner_top_right():
        return "╗"

    @staticmethod
    def corner_bottom_left():
        return "╚"

    @staticmethod
    def corner_bottom_right():
        return "╝"

    @classmethod
    def create_box(cls, text, width=76):
        """Create a box around text"""
        lines = text.split('\n')
        box = cls.corner_top_left() + cls.border_horizontal(width) + cls.corner_top_right() + "\n"

        for line in lines:
            if line.strip():
                padding = width - len(line)
                left_pad = padding // 2
                right_pad = padding - left_pad
                box += f"{cls.border_vertical()}{' ' * left_pad}{line}{' ' * right_pad}{cls.border_vertical()}\n"

        box += cls.corner_bottom_left() + cls.border_horizontal(width) + cls.corner_bottom_right()
        return box
