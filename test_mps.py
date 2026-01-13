import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"MPS available: {torch.backends.mps.is_available()}")
print(f"MPS built: {torch.backends.mps.is_built()}")

if torch.backends.mps.is_available():
    print("\n✅ MPS (Apple Silicon GPU) is available!")
    print("You can use GPU acceleration on your M4 Mac.")
    
    # Test creating a tensor on MPS
    try:
        device = torch.device("mps")
        x = torch.randn(3, 3).to(device)
        print(f"\n✅ Successfully created tensor on MPS device:")
        print(f"Device: {x.device}")
    except Exception as e:
        print(f"\n❌ Error creating tensor on MPS: {e}")
else:
    print("\n❌ MPS is not available on this system")

