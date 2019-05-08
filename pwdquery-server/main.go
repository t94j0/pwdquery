package main

import (
	"net/http"

	"github.com/t94j0/pwdquery-server/store"

	"github.com/gin-gonic/gin"
	_ "github.com/jinzhu/gorm/dialects/postgres"
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

func main() {
	var err error

	r := gin.Default()
	db, err = store.New()
	if err != nil {
		panic(err)
	}
	defer db.Close()

	r.GET("/hashes/:identifier", hashesHandler)
	r.GET("/passwords/:identifier", passwordsHandler)
	r.GET("/identifiers/:password", identifiersHandler)
	r.Run(":1234")
}
