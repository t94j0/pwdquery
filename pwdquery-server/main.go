package main

import (
	"bufio"
	"encoding/json"
	"fmt"
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
		panic(err)
	}
	c.JSON(http.StatusOK, hashes)
}

func passwordsHandler(c *gin.Context) {
	identifier := c.Param("identifier")
	passwords, err := db.GetPasswords(identifier)
	if err != nil {
		panic(err)
	}
	c.JSON(http.StatusOK, passwords)
}

func identifiersHandler(c *gin.Context) {
	password := c.Param("password")
	identifiers, err := db.GetIdentifiers(password)
	if err != nil {
		panic(err)
	}
	c.JSON(http.StatusOK, identifiers)
}

func uploadCSVHandler(c *gin.Context) {
	name, _ := c.GetPostForm("name")
	delimiterS, _ := c.GetPostForm("delimiter")
	fmt.Println("Delim:", delimiterS)
	delimiter, err := strconv.Atoi(delimiterS)
	if err != nil {
		panic(err)
	}
	skipFirstS, _ := c.GetPostForm("skip")
	skipFirst := skipFirstS == "true"

	type index struct {
		Identifier int
		Email      int
		Hash       int
		Password   int
	}
	var indicies index
	indiciesS, _ := c.GetPostForm("indicies")
	if err := json.Unmarshal([]byte(indiciesS), &indicies); err != nil {
		panic(err)
	}
	fmt.Println(indicies)

	filename, err := c.FormFile("file")
	if err != nil {
		panic(err)
	}
	file, err := filename.Open()
	if err != nil {
		panic(err)
	}
	fmt.Println(name)

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
			Identifier: entries[indicies.Identifier],
			Email:      entries[indicies.Email],
			Hash:       entries[indicies.Hash],
			Password:   entries[indicies.Password],
		}
		db.Insert(dump)
	}
	if err := scanner.Err(); err != nil {
		panic(err)
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
		panic(err)
	}
	defer db.Close()

	r.GET("/hashes/:identifier", hashesHandler)
	r.GET("/passwords/:identifier", passwordsHandler)
	r.GET("/identifiers/:password", identifiersHandler)
	r.POST("/upload-csv", uploadCSVHandler)

	fmt.Println("Listening on port 1234")
	r.Run(":1234")
}
