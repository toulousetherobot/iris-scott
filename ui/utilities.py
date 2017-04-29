from pygame import *
from copy import deepcopy
from datetime import datetime

from . import settings
from . import fonts
from . import colours
from . import state

BUTTON_HEADER = 100

def TransparentRect(surface, rect, color, transparency=64):
    rect = Rect(rect)
    color = Color(*color)
    color.a = transparency

    s = Surface(rect.size, SRCALPHA)
    s.fill(color)
    surface.blit(s, rect.topleft)

def Header(surface, robot, title, color=colours.WHITE, bg_color=colours.SCREEN_BG_COLOR, transparency=False):

    rect = Rect(0,0, settings.WINDOWWIDTH, settings.UI_MARGIN_TOP)
    if (transparency):
        TransparentRect(surface, rect, bg_color)
    else:
        draw.rect(surface, bg_color, rect)

    title_text_surf = fonts.SF_UI_DISPLAY_HEAVY.render(title, True, color)
    title_text_rect = title_text_surf.get_rect()
    title_text_rect.midleft = (settings.UI_MARGIN_LEFT, settings.UI_MARGIN_TOP/2)
    surface.blit(title_text_surf, title_text_rect)

    # Time
    now = datetime.now()
    time_text_surf = fonts.SF_UI_DISPLAY_LIGHT.render(now.strftime(settings.TIME_STRING), True, color)
    time_text_rect = time_text_surf.get_rect()
    time_text_rect.midright = (settings.WINDOWWIDTH -settings.UI_MARGIN_RIGHT, settings.UI_MARGIN_TOP/2)
    surface.blit(time_text_surf, time_text_rect)

    # Notifcation Dot
    if (robot.message_unread_count > 0 and robot.page != state.Page.MESSAGES_LIST_SCREEN and robot.page != state.Page.MESSAGE_SCREEN):
        FilledCircle(surface, (settings.WINDOWWIDTH/2, settings.UI_MARGIN_TOP/2, settings.NOTIFICATION_RADIUS), colours.ERROR_RED)

    return {"target": title_text_rect, "value": BUTTON_HEADER}


def FilledCircle(surface, circ, color):

    """
    FilledRoundedRectangle(surface, rect, color)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    """

    rect         = Rect((circ[0]-circ[2]/2, circ[1]-circ[2]/2, circ[2], circ[2]))
    color        = Color(*color)
    color.a      = 0
    rectangle    = Surface(rect.size, SRCALPHA, depth=32)

    circle = Surface([min(rect.size)*3]*2, SRCALPHA, depth=32)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle = transform.smoothscale(circle,[int(min(rect.size))]*2)
    rectangle.blit(circle,(0,0))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    surface.blit(rectangle, rect.topleft)

    return rect

def FilledRoundedRectangle(surface, rect, color, radius=0.4):

    """
    FilledRoundedRectangle(surface, rect, color, radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    original_rect = deepcopy(rect)
    original_color = deepcopy(color)
    if isinstance(color, list):
        color        = Color("white")
    else: 
        color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = Surface(rect.size, SRCALPHA, depth=32)
    gradient    = Surface(rect.size, SRCALPHA, depth=32)

    circle       = Surface([min(rect.size)*3]*2, SRCALPHA, depth=32)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    # Mask Gradient with Rounded
    if isinstance(original_color, list):
        FillGradient(gradient, original_color[0], original_color[1])
        gradient.blit(rectangle, (0, 0), None, BLEND_RGBA_MULT)
        surface.blit(gradient, pos)
    else:
        surface.blit(rectangle, pos)
    return original_rect

def FillGradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse
    
    Pygame recipe: http://www.pygame.org/wiki/GradientCode
    """
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    rate = (
        float(b[0]-a[0])/h,
        float(b[1]-a[1])/h,
        float(b[2]-a[2])/h
    )
    fn_line = draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def DrawTextBox(surface, text, color, rect, font, aa = False, bkg = None):

    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text