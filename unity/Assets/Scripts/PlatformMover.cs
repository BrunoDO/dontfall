using UnityEngine;

public class PlatformMover : MonoBehaviour
{
    public float speed = 4f;

    void Update()
    {
        // Move upward
        transform.Translate(Vector3.up * speed * Time.deltaTime);

        // Destroy when off-screen (Top is roughly Y = 6)
        if (transform.position.y > 6.5f)
        {
            Destroy(gameObject);
        }
    }
}