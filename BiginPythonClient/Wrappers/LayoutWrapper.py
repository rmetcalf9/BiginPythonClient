from .BaseWrapper import ArrayWrapper, BaseWrapper
from ..BiginModules import Module
import json

def layoutWrapperFactory(client, loginSession, dict, layout_module):
    if layout_module==Module.PIPELINES:
        return PipelinesLayoutWrapper(client, loginSession, dict, layout_module)
    return OtherLayoutWrapper(client, loginSession, dict, layout_module)

class BaseLayoutWrapper(ArrayWrapper):
    layout_module = None
    def __init__(self, client, loginSession, dict, layout_module):
        super().__init__(client, loginSession, dict, "layouts")
        self.layout_module = layout_module

class OtherLayoutWrapper(BaseLayoutWrapper):
    pass

class PipelinesLayoutWrapper(BaseLayoutWrapper):
    def itemFactory(self, item):
        return PipelineWrapper(client=self.client, loginSession=self.loginSession, dict=item)
    def getPipeline(self, name):
        for pipeline in self.items:
            if pipeline.dict["name"] == name:
                return pipeline
        return None

class PipelineWrapper(BaseWrapper):
    sections = None
    def __init__(self, client, loginSession, dict):
        super().__init__(client, loginSession, dict)
        self.sections = PipelineSectionsWrapper(client, loginSession, self.dict, "sections")

    def getStages(self):
        field = self.getField("Stage")
        if field is None:
            return None
        stages = []
        for x in field.getPickListValues():
            stages.append({
                "id": x["id"],
                "display_value": x["display_value"],
                "reference_value": x["reference_value"],
                "sequence_number": x["sequence_number"],
                "actual_value": x["actual_value"]
            })
        stages = sorted(stages, key=lambda d: d['sequence_number'])
        return stages

    def getFields(self):
        section = self.sections.getSection("Potential Information")
        if section is None:
            return None
        return section.fields

    def getField(self, api_name):
        return self.getFields.getField(api_name)

    def getRecordPage(self, fields, page):
        params = {
            #"per_page": "1",
            "page": page
        }
        if fields is not None:
            params["fields"] = fields

        result = self.client.sendGetRequest(
            url="/" + Module.PIPELINES.value,
            loginSession=self.loginSession,
            injectHeadersFn=None,
            params=params
        )
        if result.status_code != 200:
            self.client.raiseResponseException(result)
        response = json.loads(result.text)
        return (response["info"]["more_records"], response["data"])

    def getRecords(self, fields=None):
        page = 1
        while True:
            (has_more, items) = self.getRecordPage(fields, page)
            for item in items:
                yield item
            if not has_more:
                break
            page += 1

class PipelineSectionsWrapper(ArrayWrapper):
    def itemFactory(self, item):
        return PipelineSectionWrapper(self.client, self.loginSession, item)
    def getSection(self, name):
        for section in self.items:
            if section.dict["name"] == name:
                return section
        return None

class PipelineSectionWrapper(BaseWrapper):
    fields = None
    def __init__(self, client, loginSession, dict):
        super().__init__(client, loginSession, dict)
        self.fields = PipelineFieldsWrapper(client, loginSession, self.dict, "fields")

class PipelineFieldsWrapper(ArrayWrapper):
    def itemFactory(self, item):
        return PipelineFieldWrapper(self.client, self.loginSession, item)
    def getField(self, api_name):
        for field in self.items:
            if field.dict["api_name"] == api_name:
                return field
        return None


class PipelineFieldWrapper(BaseWrapper):
    def getPickListValues(self):
        return self.dict["pick_list_values"]