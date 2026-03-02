using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;
using System.Collections;

public class GameManager : MonoBehaviour
{
    public static GameManager instance;

    [Header("UI Panels")]
    public GameObject startMenuUI;
    public GameObject gameOverUI;

    [Header("State")]
    public bool isGameStarted = false;
    public bool isGameOver = false;

    [Header("Score")]
    public TMP_Text scoreText;
    public TMP_Text highScoreText;
    public TMP_Text MhighScoreText;
    public TMP_Text comboText;
    public int score = 0;
    public int highScore = 0;

    [Header("Game Over")]
    public TMP_Text goScore;
    public TMP_Text goCombos;
    public TMP_Text goTotal;

    private Coroutine comboRoutine;
    //private int comboTotal = 0;

    private void Awake()
    {
        PlayerPrefs.SetInt("ComboTotal", 0);
        if (instance != null && instance != this)
        {
            Destroy(gameObject);
            return;
        }

        instance = this;

        score = 0;
        highScore = PlayerPrefs.GetInt("HighScore", 0);

        Time.timeScale = 1f;
        isGameStarted = false;
        isGameOver = false;

        if (startMenuUI != null)
            startMenuUI.SetActive(true);

        if (gameOverUI != null)
            gameOverUI.SetActive(false);

        if (comboText != null)
            comboText.gameObject.SetActive(false);

        UpdateScoreUI();
    }

    private void Start()
    {
        StartCoroutine(RefreshMenuTextNextFrame());
    }

    private IEnumerator RefreshMenuTextNextFrame()
    {
        yield return null;
        UpdateScoreUI();
    }

    void Update()
    {
        bool anyKeyPressed = Keyboard.current != null && Keyboard.current.anyKey.wasPressedThisFrame;

        if (anyKeyPressed)
        {
            if (!isGameStarted && !isGameOver) StartGame();
            else if (isGameOver) RestartGame();
        }
    }

    public void StartGame()
    {
        isGameStarted = true;
        if (startMenuUI != null) startMenuUI.SetActive(false);
        UpdateScoreUI();
    }

    public void EndGame()
    {
        if (isGameOver) return;

        isGameOver = true;
        isGameStarted = false;

        //score = score * PlayerPrefs.GetInt("ComboTotal",0);

        if (score > highScore)
        {
            highScore = score;
            PlayerPrefs.SetInt("HighScore", highScore);
            PlayerPrefs.Save();
        }

        if (gameOverUI != null) gameOverUI.SetActive(true);
        Time.timeScale = 0f;

        //Game over scoring
        goScore.text = "Score: " + score;
        goCombos.text = "Combos: x" + PlayerPrefs.GetInt("ComboTotal", 0);
        goTotal.text = "Total: " + score * PlayerPrefs.GetInt("ComboTotal", 0); 

        UpdateScoreUI();
    }

    public void RestartGame()
    {
        Time.timeScale = 1f;
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

    public void AddScore(int amount)
    {
        score += amount;

        if (score > highScore)
        {
            highScore = score;
            PlayerPrefs.SetInt("HighScore", highScore);
            PlayerPrefs.Save();
            PopScoreUI(highScoreText);
        }

        UpdateScoreUI();
        PopScoreUI(scoreText);
    }

    public void UpdateScoreUI()
    {
        if (scoreText != null)
            scoreText.text = "Score: " + score;

        if (highScoreText != null)
            highScoreText.text = "High Score: " + highScore;

        if (MhighScoreText != null)
            MhighScoreText.text = "High Score: " + highScore;
    }

    public void PopScoreUI(TMP_Text t)
    {
        if (t == null) return;

        StartCoroutine(PopRoutine(t.transform));
        StartCoroutine(FloatAndFade(t));
    }

    private IEnumerator PopRoutine(Transform t)
    {
        Vector3 start = t.transform.localScale;
        Vector3 big = start * 2f;

        t.localScale = big;

        float time = 0f;
        float duration = 0.12f;

        while (time < duration)
        {
            t.localScale = Vector3.Lerp(big, start, time / duration);
            time += Time.unscaledDeltaTime;
            yield return null;
        }

        t.localScale = start;
    }

    private IEnumerator FloatAndFade(TMP_Text text)
    {
        float time = 0f;
        float duration = 0.25f;

        Vector3 startPos = text.transform.localPosition;
        Vector3 endPos = startPos + Vector3.up * 12f;

        Color startColor = text.color;
        Color endColor = new Color(startColor.r, startColor.g, startColor.b, 0.6f);

        while (time < duration)
        {
            float t = time / duration;
            text.transform.localPosition = Vector3.Lerp(startPos, endPos, t);
            text.color = Color.Lerp(startColor, endColor, t);
            time += Time.unscaledDeltaTime;
            yield return null;
        }

        text.transform.localPosition = startPos;
        text.color = startColor;
    }

    public void ShowComboText(int combo)
    {
        if (comboText == null) return;

        comboText.text = "x" + combo;
        comboText.gameObject.SetActive(true);

        if (comboRoutine != null)
            StopCoroutine(comboRoutine);

        comboRoutine = StartCoroutine(HideComboRoutine());
    }

    private IEnumerator HideComboRoutine()
    {
        yield return new WaitForSeconds(0.7f);
        comboText.gameObject.SetActive(false);
    }

    public void ResetButton()
    {
        PlayerPrefs.SetInt("HighScore", 0);
        highScore = 0;
        highScoreText.text = "High Score: 0";
        MhighScoreText.text = "High Score: 0";
    }
}
