using UnityEngine;

public class PlatformSpawner : MonoBehaviour
{

    [System.Serializable]
    public class WeightedPlatform
    {
        public GameObject prefab;
        [Range(0f, 100f)] public float weight = 50f;
    }

    [Header("Platform Rarity Weights")]
    public WeightedPlatform[] platforms;

    [Header("Prefabs and References")]
    public GameObject platformPrefab;
    public Transform player;


    [Header("Spawning Settings")]
    public float spawnDistance = 10f;
    public float distanceBetweenPlatforms = 4f;
    public float xRange = 5f;

    private float nextSpawnY = 2f; // Starts above the initial manual platform

    [SerializeField] int startingPlatforms = 5;



    void Start()
    {
        // Pre-spawn the "Ladder" (first 5 platforms)
        //SpawnPlatformAtX(0f);
        for (int i = 0; i < startingPlatforms; i++)
        {
            SpawnPlatform();
        }
    }

    void Update()
    {
        if (player == null || !GameManager.instance.isGameStarted) return;

        // Keep spawning new platforms at the top as the player climbs
        while (player.position.y + spawnDistance > nextSpawnY)
        {
            SpawnPlatform();
        }
    }

    void SpawnPlatform()
    {
        Vector3 spawnPos = new Vector3(Random.Range(-xRange, xRange), nextSpawnY, 0);

        float difficultyBoost = nextSpawnY * 0.02f;

        platforms[0].weight = 50f - difficultyBoost; // Base
        platforms[1].weight = 25f - difficultyBoost;  // Grass
        platforms[2].weight = 15f + difficultyBoost; // Wood breakable
        platforms[3].weight = 10f + difficultyBoost;  // Ice
        platforms[3].weight = 5f + difficultyBoost;  // fire

        GameObject prefab = GetRandomPlatform();
        Instantiate(prefab, spawnPos, Quaternion.identity);

        nextSpawnY += distanceBetweenPlatforms;
        Debug.Log("Spawned: " + prefab.name);

    }


    GameObject GetRandomPlatform()
    {
        float totalWeight = 0f;
        foreach (var p in platforms)
            totalWeight += p.weight;

        float roll = Random.Range(0f, totalWeight);
        float current = 0f;

        foreach (var p in platforms)
        {
            current += p.weight;
            if (roll <= current)
                return p.prefab;
        }

        return platforms[0].prefab; // fallback
    }
}