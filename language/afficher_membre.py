from .layout import Layout

class AfficherMembre:

    content_fr={"page_title":"Voici les détails du membres"}
    lay_fr=Layout.layout_fr
    lay_en=Layout.layout_en
    fr=content_fr.update(lay_fr)
    content_en={"page_title":"Member details"}
    en=content_en.update(lay_en)