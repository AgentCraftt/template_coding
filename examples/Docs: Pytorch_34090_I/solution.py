import torch


def process_dlpack_tensor(dlpack_tensor):
    """
    Given a tensor in DLPack format, convert it to a PyTorch tensor,
    perform normalization, square it, transpose it, and convert back to DLPack format.
    """
    # 1. Convert DLPack tensor to PyTorch tensor
    pytorch_tensor = torch.utils.dlpack.from_dlpack(dlpack_tensor)

    # 2. Normalize the tensor between 0 and 1
    normalized_tensor = (pytorch_tensor - pytorch_tensor.min()) / (
        pytorch_tensor.max() - pytorch_tensor.min()
    )

    # 3. Square the normalized tensor element-wise
    squared_tensor = normalized_tensor**2

    # 4. Transpose the squared tensor
    transposed_tensor = squared_tensor.transpose(0, 1)

    # 5. Convert the final PyTorch tensor back to DLPack format
    final_dlpack_tensor = torch.utils.dlpack.to_dlpack(transposed_tensor)

    return final_dlpack_tensor
