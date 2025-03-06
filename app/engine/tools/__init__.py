import importlib
import os
from typing import Dict, List, Union

import yaml
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec


class ToolFactory:
    @staticmethod
    def load_tools(tool_name: str, config: dict) -> List[FunctionTool]:
        source_package = "app.engine.tools"
        try:
            if "ToolSpec" in tool_name:
                tool_package, tool_cls_name = tool_name.split(".")
                module_name = f"{source_package}.{tool_package}"
                module = importlib.import_module(module_name)
                tool_class = getattr(module, tool_cls_name)
                tool_spec: BaseToolSpec = tool_class(**config)
                return tool_spec.to_tool_list()
            else:
                module = importlib.import_module(f"{source_package}.{tool_name}")
                tools = module.get_tools(**config)
                if not all(isinstance(tool, FunctionTool) for tool in tools):
                    raise ValueError(
                        f"Модуль {module} не содержит действительных инструментов"
                    )
                return tools
        except ImportError as e:
            raise ValueError(f"Не удалось импортировать инструмент {tool_name}: {e}")
        except AttributeError as e:
            raise ValueError(f"Не удалось загрузить инструмент {tool_name}: {e}")

    @staticmethod
    def from_env(
            map_result: bool = False,
    ) -> Union[Dict[str, List[FunctionTool]], List[FunctionTool]]:

        tools: Union[Dict[str, FunctionTool], List[FunctionTool]] = (
            {} if map_result else []
        )

        if os.path.exists("config/tools.yaml"):
            with open("config/tools.yaml", "r") as f:
                tool_configs = yaml.safe_load(f)
                if tool_configs:
                    for tool_name, config in tool_configs.items():
                        loaded_tools = ToolFactory.load_tools(
                            tool_name,
                            config,
                        )
                        if map_result:
                            tools.update(  # type: ignore
                                {tool.metadata.name: tool for tool in loaded_tools}
                            )
                        else:
                            tools.extend(loaded_tools)  # type: ignore

        return tools
