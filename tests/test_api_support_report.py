import json
from pathlib import Path


HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
DATA_DIR = Path(__file__).parent / "test_data"


def _manifest_operations(path: Path) -> set[tuple[str, str]]:
    data = json.loads(path.read_text())
    return {
        (method.upper(), route.rstrip("/").lower())
        for method, route in data["supported_operations"]
    }


def _swagger_operations(path: Path) -> set[tuple[str, str]]:
    swagger = json.loads(path.read_text())
    return {
        (method.upper(), route.rstrip("/").lower())
        for route, operations in swagger["paths"].items()
        for method in operations
        if method.upper() in HTTP_METHODS
    }


def test_api_support_report():
    swagger_operations = _swagger_operations(DATA_DIR / "cyberark-pvwa-swagger.json")
    supported_operations = _manifest_operations(DATA_DIR / "support_manifest.json")
    baseline_operations = _manifest_operations(
        DATA_DIR / "support_manifest_baseline.json"
    )

    invalid_operations = supported_operations - swagger_operations
    removed_operations = baseline_operations - supported_operations
    assert not invalid_operations, (
        "Manifest entries absent from Swagger: "
        f"{sorted(invalid_operations)}"
    )
    assert not removed_operations, (
        "Supported operations were removed: " f"{sorted(removed_operations)}"
    )

    percentage = len(supported_operations) / len(swagger_operations) * 100
    print("## CyberArk PVWA API support")
    print(f"Implemented: {len(supported_operations)} / {len(swagger_operations)}")
    print(f"Coverage: {percentage:.1f}%")
    print(f"Unimplemented: {len(swagger_operations - supported_operations)}")