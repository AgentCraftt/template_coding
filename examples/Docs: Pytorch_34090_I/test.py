import torch
import numpy as np

from solution import process_dlpack_tensor


def test_process_dlpack_tensor():
    # Create a PyTorch tensor and convert it to DLPack
    input_tensor = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
    input_dlpack_tensor = torch.utils.dlpack.to_dlpack(input_tensor)

    # Process the DLPack tensor
    output_dlpack_tensor = process_dlpack_tensor(input_dlpack_tensor)

    # Convert the output DLPack tensor back to a PyTorch tensor for verification
    output_tensor = torch.utils.dlpack.from_dlpack(output_dlpack_tensor)

    # Expected output tensor after processing
    expected_output_tensor = torch.tensor(
        [[0.0000, 0.4444], [0.1111, 1.0000]], dtype=torch.float32
    )

    assert torch.allclose(output_tensor, expected_output_tensor, atol=1e-4), (
        f"{output_tensor} != {expected_output_tensor}"
    )


def test_process_dlpack_tensor_with_different_shape():
    # Test with a different shaped tensor
    input_tensor = torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=torch.float32)
    input_dlpack_tensor = torch.utils.dlpack.to_dlpack(input_tensor)

    output_dlpack_tensor = process_dlpack_tensor(input_dlpack_tensor)

    output_tensor = torch.utils.dlpack.from_dlpack(output_dlpack_tensor)

    # Calculate expected output manually
    normalized_tensor = (input_tensor - input_tensor.min()) / (
        input_tensor.max() - input_tensor.min()
    )
    expected_output_tensor = (normalized_tensor**2).transpose(0, 1)

    assert torch.allclose(output_tensor, expected_output_tensor, atol=1e-4), (
        f"{output_tensor} != {expected_output_tensor}"
    )
