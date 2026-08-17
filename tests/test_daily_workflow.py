from workflows.daily_0900 import _default_collectors


def test_default_collectors_apply_bitrix24_field_mapping() -> None:
    collectors = _default_collectors(
        {
            "bitrix24": {
                "entity_type_id": 1,
                "field_mapping": {
                    "created_at": "createdTime",
                    "updated_at": "updatedTime",
                    "source_type": "sourceId",
                    "phone": "ufCrmLeadPhone",
                },
            }
        }
    )

    bitrix24 = collectors[0]

    assert bitrix24.entity_type_id == 1
    assert bitrix24.field_map.phone == "ufCrmLeadPhone"
