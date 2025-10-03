from modeltranslation.translator import register, TranslationOptions
from .models import GetStarted, Xizmatlar, XizmatVariant, Qurilma


@register(GetStarted)
class GetStartedTranslationOptions(TranslationOptions):
    fields = ('title', 'desc')


@register(Xizmatlar)
class XizmatlarTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(XizmatVariant)
class XizmatVariantTranslationOptions(TranslationOptions):
    fields = ('title','desc')

    
@register(Qurilma)
class QurilmaTranslationOptions(TranslationOptions):
    fields = ('name', 'desc')
