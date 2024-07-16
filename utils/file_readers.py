import xml.etree.ElementTree as ET

from models.storage_entity import StorageEntity


def write_config_file(data: dict[str, StorageEntity], path: str):
    """
    creates the config file with the data provided at the specified location
    :param data:
    :param path:
    :return:
    """

    def createComponent(parentElement: ET.Element, entity: StorageEntity):
        component = ET.SubElement(parentElement, "component")

        component.set("pid", str(entity.key()))

        if entity.value() is None:
            component.set('value', "none")
            return

        if isinstance(entity.value(), int) or isinstance(entity.value(), float):
            component.set('value', str(entity.value()))
            return

        if isinstance(entity.value(), str):
            component.set('value', entity.value())
            return

    config = ET.Element('config')

    # create the components
    for storageEntity in data.values():
        createComponent(config, storageEntity)

    tree = ET.ElementTree(config)
    tree.write(path, encoding='utf-8', xml_declaration=True)


def read_config_file(path: str) -> dict[str, StorageEntity]:
    """
    reads the config file from storage
    :param path:
    :return:
    """

    res = {}

    tree = ET.parse(path)
    config = tree.getroot()

    components = config.findall("component")
    if len(components) == 0:
        return res

    def collect_component_data(element: ET.Element) -> tuple[str, StorageEntity]:
        _k = element.get('pid')

        # by default values are strings
        _v = element.get('value')

        # if the string is none
        if element.get('value') == 'none':
            _v = None

        # if the string is number
        if _k in ["fetch_interval", "joke_quantity"]:
            _v = float(element.get('value'))

        return _k, StorageEntity(_k, _v)

    for component in components:
        k, v = collect_component_data(component)
        res.update({k: v})

    return res
