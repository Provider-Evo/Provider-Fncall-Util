

from provider_sdk import ProviderPlugin
from provider_sdk.extensions.fncall import FncallPluginMixin


class FncallUtilPlugin(ProviderPlugin, FncallPluginMixin):
    async def on_load(self) -> None:
        from echotools.exec.protocol.base import register_protocol
        from provider_fncall_util.protocols.antml import AntmlProtocol
        from provider_fncall_util.protocols.bracket import BracketProtocol
        from provider_fncall_util.protocols.extra.custom import CustomProtocol
        from provider_fncall_util.protocols.dsml import DsmlProtocol
        from provider_fncall_util.protocols.nous import NousProtocol
        from provider_fncall_util.protocols.extra.origin import OriginalProtocol
        from provider_fncall_util.protocols.xml import XmlProtocol

        for proto in (
            XmlProtocol(),
            AntmlProtocol(),
            OriginalProtocol(),
            BracketProtocol(),
            NousProtocol(),
            DsmlProtocol(),
        ):
            register_protocol(proto)

        factory = lambda prompt_en="", prompt_zh="": CustomProtocol(
            prompt_en=prompt_en, prompt_zh=prompt_zh
        )
        self.register_custom_protocol_factory(factory)
        try:
            from src.core.fncall.reg import set_custom_protocol_factory

            set_custom_protocol_factory(factory)
        except ImportError:
            pass
        self.ctx.logger.info(
            "Provider-Fncall-Util: xml/antml/original/bracket/nous/dsml/custom registered"
        )

    async def on_unload(self) -> None:
        from echotools.exec.protocol.base import unregister_protocol

        for protocol_id in (
            "xml",
            "antml",
            "original",
            "bracket",
            "nous",
            "dsml",
        ):
            unregister_protocol(protocol_id)
        try:
            from src.core.fncall.reg import clear_custom_protocol_factory

            clear_custom_protocol_factory()
        except ImportError:
            pass
        self._custom_protocol_factory = None
        self.ctx.logger.info("Provider-Fncall-Util: fncall protocols unregistered")


def create_plugin() -> FncallUtilPlugin:
    return FncallUtilPlugin()

__all__ = []
