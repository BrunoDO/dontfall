using UnityEngine;

public class Platform : MonoBehaviour
{
    private float speed;
    private float width = 3f;
    private SpriteRenderer sr;

    // This runs the very first frame the platform exists
    void Start()
    {
        ;
        Initialize(GameManager.instance.score);
        
        
        // Start at size zero so it can "pop" in
        //transform.localScale = Vector3.zero;
    }

    public void Initialize(int score)
    {
        //speed = 3f + (score * 0.15f);
        width = Mathf.Max(3f - (score * 0.1f), 1.2f); // Increased floor to 1.2 for visibility
        
        //sr = GetComponent<SpriteRenderer>();
        //if (sr.material.HasProperty("_Glossiness"))
        //{
        //    sr.material.SetFloat("_Glossiness", 0f);
        //}
        //float t = Mathf.InverseLerp(1f, 50f, score);
        //Color neonColor = Color.HSVToRGB(Mathf.Lerp(0.5f, 0.0f, t), 1f, 1f);


        // Force the color on both the renderer AND the material
        //sr.color = neonColor;

        //// If your shader has a '_MainColor' or '_BaseColor' property
        //if (sr.material.HasProperty("_Color"))
        //    sr.material.SetColor("_Color", neonColor);
        //else if (sr.material.HasProperty("_BaseColor"))
        //    sr.material.SetColor("_BaseColor", neonColor);

        // Ensure it's not being darkened by shadows
        
    }


    void Update()
    {
        // Move upward
        //transform.position += Vector3.down * speed * Time.deltaTime;

        // THE FIX: Keep Y at a constant 1.0f (or whatever looks best for your sprite)
        // Only the 'width' variable should change based on the score
        Vector3 targetScale = new Vector3(width, 1.0f, 1.0f);

        //SNAPPY
        //transform.localScale = Vector3.Lerp(transform.localScale, targetScale, Time.deltaTime * 12f);
        //floaty
        transform.localScale = Vector3.MoveTowards(transform.localScale,targetScale,Time.deltaTime * 5f);


        //if (transform.position.y < -10f) Destroy(gameObject);
    }

    public float GetSpeed()
    {
        return speed;
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        // If this platform hits the "DeathZone" trigger attached to the camera
        if (collision.gameObject.CompareTag("DeathZone"))
        {
            Destroy(gameObject);
        }
    }
}