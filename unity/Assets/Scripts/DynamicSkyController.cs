using UnityEngine;

public class DynamicSkyController : MonoBehaviour
{
    private MeshRenderer mr;
    private PlayerController player;

    void Start()
    {
        mr = GetComponent<MeshRenderer>();
        player = Object.FindFirstObjectByType<PlayerController>();

        // This forces the Quad to show exactly 1/4th of the image (one tile)
        mr.material.mainTextureScale = new Vector2(0.25f, 0.25f);
    }

    void Update()
    {
        if (player == null) return;

        // Simplified math for a 4x4 grid
        int tileIndex = Mathf.Clamp(GameManager.instance.score/ 5, 0, 15);

        float x = (tileIndex % 4) * 0.25f;
        float y = (tileIndex / 4) * 0.25f;

        // IMPORTANT: Unity UI/Textures coordinates start from BOTTOM-LEFT.
        // If your "Day" is at the top of the PNG, we need to invert Y:
        float invertedY = 0.75f - y;

        mr.material.mainTextureOffset = new Vector2(x, invertedY);
    }
}