using UnityEngine;
using UnityEngine.InputSystem;
using System.Collections.Generic;

public class PlayerController : MonoBehaviour
{
    public static PlayerController instance;
    public float moveSpeed = 8f;
    public float jumpForce = 12f;

    private Rigidbody2D rb;
    public bool isGrounded = false;

    private HashSet<GameObject> scoredPlatforms = new HashSet<GameObject>();

    [Header("Combo")]
    public float comboTime = 1.2f;
    private int comboCount = 1;
    private float lastLandTime = 0f;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        rb.simulated = false;
    }

    void Update()
    {
        if (GameManager.instance == null || !GameManager.instance.isGameStarted) return;

        rb.simulated = true;

        float moveInput = 0f;

        if (Keyboard.current != null)
        {
            if (Keyboard.current.aKey.isPressed || Keyboard.current.leftArrowKey.isPressed) moveInput = -1;
            if (Keyboard.current.dKey.isPressed || Keyboard.current.rightArrowKey.isPressed) moveInput = 1;
        }

        rb.linearVelocity = new Vector2(moveInput * moveSpeed, rb.linearVelocity.y);

        if (isGrounded && Keyboard.current != null)
        {
            if (Keyboard.current.upArrowKey.wasPressedThisFrame || Keyboard.current.spaceKey.wasPressedThisFrame)
            {
                rb.AddForce(Vector2.up * jumpForce, ForceMode2D.Impulse);
                isGrounded = false;
            }
        }
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (!collision.gameObject.CompareTag("Platform"))
            return;

        if (rb.linearVelocity.y > 0f)
            return;

        ContactPoint2D contact = collision.contacts[0];
        bool landedFromAbove = contact.normal.y > 0.5f;

        if (!landedFromAbove)
            return;

        isGrounded = true;

        // Platform behavior hook
        PlatformBase platform = collision.gameObject.GetComponent<PlatformBase>();
        if (platform != null)
        {
            platform.OnPlayerLanded(this);
        }

        if (scoredPlatforms.Contains(collision.gameObject))
            return;

        scoredPlatforms.Add(collision.gameObject);

        float timeSinceLastLand = Time.time - lastLandTime;

        if (timeSinceLastLand <= comboTime)
            comboCount++;
        else
            comboCount = 1;

        lastLandTime = Time.time;

        if (comboCount > 1)
        {
            GameManager.instance.ShowComboText(comboCount);
            int cTotal = PlayerPrefs.GetInt("ComboTotal", 0);
            PlayerPrefs.SetInt("ComboTotal", cTotal + comboCount);
        }

        GameManager.instance.AddScore(1);
    }

    private void OnCollisionExit2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Platform"))
            isGrounded = false;
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.CompareTag("DeathZone"))
            GameManager.instance.EndGame();
    }
}
