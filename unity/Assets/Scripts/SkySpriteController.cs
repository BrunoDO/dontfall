using UnityEngine;

public class SkySpriteController : MonoBehaviour
{
    private MeshRenderer mr;
    public PlayerController player;
    public float scrollSpeed = 0.1f;

    void Start()
    {
        mr = GetComponent<MeshRenderer>();
        // Sets tiling to see only 1/4th of the vertical texture (assuming 4 colors)
        mr.material.mainTextureScale = new Vector2(1f, 0.25f);
    }

    void Update()
    {
        if (player == null) return;

        // Use the score we just added back to move the sky
        float targetY = GameManager.instance.score * 0.02f;
        float currentY = mr.material.mainTextureOffset.y;

        float newY = Mathf.MoveTowards(currentY, targetY, Time.deltaTime * scrollSpeed);
        mr.material.mainTextureOffset = new Vector2(0, newY);
    }
}