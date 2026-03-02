using UnityEngine;
using UnityEngine.Jobs;

public class CameraFollow : MonoBehaviour
{
    public Transform target; // Drag Player here
    public float smoothSpeed = 10f;
    [SerializeField] public float baseSpeed = 1f;
    [SerializeField] public float speedPerScore = 0.5f;
    [SerializeField] public float maxSpeed = 100f;
    public float followSmooth = 0.1f;
    private float currentYVelocity;

    void Update()
    {
        if (target == null || !GameManager.instance.isGameStarted) return;

        float speed = baseSpeed + GameManager.instance.score * speedPerScore;
        speed = Mathf.Min(speed, maxSpeed);
        Debug.Log("Speed: " + speed);

        float desiredY = transform.position.y + speed * Time.deltaTime;


        if (desiredY < target.position.y)
            desiredY = target.position.y;

        float smoothY = Mathf.SmoothDamp(transform.position.y, desiredY, ref currentYVelocity, followSmooth);

        transform.position = new Vector3(transform.position.x, smoothY, transform.position.z);

        Debug.Log("Transform y: " + transform.position.y);
    }




    void LateUpdate()
    {
        //if (target == null) return;

        //// Only follow the player if they move HIGHER than the camera's current position
        //if (target.position.y > transform.position.y)
        //{
        //    float yOffset = 2f;
        //    Vector3 targetPosition = new Vector3(transform.position.x, target.position.y + yOffset, transform.position.z);
        //    Vector3 velocity = Vector3.zero;
        //    transform.position = Vector3.SmoothDamp(transform.position, targetPosition, ref velocity, smoothSpeed);
        //}

    }
}