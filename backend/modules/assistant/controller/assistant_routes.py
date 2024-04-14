from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.assistant.dto.inputs import InputAssistant
from modules.assistant.dto.outputs import AssistantOutput
from modules.assistant.ito.difference import DifferenceAssistant, difference_inputs
from modules.assistant.ito.summary import SummaryAssistant, summary_inputs
from modules.assistant.service.assistant import Assistant
from modules.user.entity.user_identity import UserIdentity

assistant_router = APIRouter()
logger = get_logger(__name__)

assistant_service = Assistant()


@assistant_router.get(
    "/assistants", dependencies=[Depends(AuthBearer())], tags=["Assistant"]
)
async def list_assistants(
    current_user: UserIdentity = Depends(get_current_user),
) -> List[AssistantOutput]:
    """
    Retrieve and list all the knowledge in a brain.
    """

    summary = summary_inputs()
    # difference = difference_inputs()
    # crawler = crawler_inputs()
    # audio_transcript = audio_transcript_inputs()
    return [summary]


@assistant_router.post(
    "/assistant/process",
    dependencies=[Depends(AuthBearer())],
    tags=["Assistant"],
)
async def process_assistant(
    input: InputAssistant,
    files: List[UploadFile] = None,
    current_user: UserIdentity = Depends(get_current_user),
):
    if input.name == "summary":
        summary_assistant = SummaryAssistant(
            input=input, files=files, current_user=current_user
        )
        try:
            summary_assistant.check_input()
            return await summary_assistant.process_assistant()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif input.name == "difference":
        difference_assistant = DifferenceAssistant(
            input=input, files=files, current_user=current_user
        )
        try:
            difference_assistant.check_input()
            return await difference_assistant.process_assistant()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Assistant not found"}
