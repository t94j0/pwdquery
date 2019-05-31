package main

import (
	"bufio"
	"encoding/json"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	_ "github.com/jinzhu/gorm/dialects/postgres"

	"github.com/t94j0/pwdquery-server/store"
)

var db *store.DB

func hashesHandler(c *gin.Context) {
	identifier := c.Param("identifier")
	hashes, err := db.GetHashes(identifier)
	if err != nil {
		log.Print("Error getting hashes: ", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "server error"})
		return
	}
	c.JSON(http.StatusOK, hashes)
}

func passwordsHandler(c *gin.Context) {
	identifier := c.Param("identifier")
	passwords, err := db.GetPasswords(identifier)
	if err != nil {
		log.Print("Error getting hashes: ", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "server error"})
		return
	}
	c.JSON(http.StatusOK, passwords)
}

func identifiersHandler(c *gin.Context) {
	password := c.Param("password")
	identifiers, err := db.GetIdentifiers(password)
	if err != nil {
		log.Print("Error getting identifiers: ", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "server error"})
		return
	}
	c.JSON(http.StatusOK, identifiers)
}

func uploadCSVHandler(c *gin.Context) {
	name, _ := c.GetPostForm("name")
	// Get delimiter as integer
	delimiterS, _ := c.GetPostForm("delimiter")
	delimiter, err := strconv.Atoi(delimiterS)
	if err != nil {
		log.Print("Error converting delimiter: ", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "server error"})
		return
	}
	// Get skip as boolean
	skipFirstS, _ := c.GetPostForm("skip")
	skipFirst := skipFirstS == "true"

	// Get index values as struct
	type index struct {
		Identifier int
		Email      int
		Hash       int
		Password   int
	}
	var indicies index
	indiciesS, _ := c.GetPostForm("indicies")
	if err := json.Unmarshal([]byte(indiciesS), &indicies); err != nil {
		log.Print("Error marshalling JSON: ", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "server error"})
		return
	}

	// Get file
	filename, err := c.FormFile("file")
	if err != nil {
		log.Print("Error getting file: ", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "server error"})
		return
	}
	file, err := filename.Open()
	if err != nil {
		log.Print("Error opening file: ", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "server error"})
		return
	}

	// Expected array length
	scanner := bufio.NewScanner(file)
	var arrayLength int
	for scanner.Scan() {
		if skipFirst {
			skipFirst = false
			continue
		}
		line := scanner.Text()
		entries := strings.Split(line, string(delimiter))
		// Clean data by ensuring expected array length is satisfied
		if arrayLength == 0 {
			arrayLength = len(entries)
		}
		if len(entries) != arrayLength {
			continue
		}
		dump := store.Dump{
			DumpID:     name,
			Identifier: entries[indicies.Identifier],
			Email:      entries[indicies.Email],
			Hash:       entries[indicies.Hash],
			Password:   entries[indicies.Password],
		}
		db.Insert(dump)
	}
	if err := scanner.Err(); err != nil {
		log.Print("Error in scanner:", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "server error"})
		return
	}
	c.JSON(http.StatusOK, "")
}

func main() {
	var err error

	gin.SetMode(gin.ReleaseMode)
	gin.DisableConsoleColor()
	r := gin.Default()

	db, err = store.New(25)
	if err != nil {
		log.Panic("Error creating store: ", err)
		return
	}
	defer db.Close()

	r.GET("/hashes/:identifier", hashesHandler)
	r.GET("/passwords/:identifier", passwordsHandler)
	r.GET("/identifiers/:password", identifiersHandler)
	r.POST("/upload-csv", uploadCSVHandler)

	log.Print("Listening on port 1234")
	r.Run(":1234")
}
