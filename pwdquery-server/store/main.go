package store

import (
	"github.com/eapache/channels"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
)

type Dump struct {
	gorm.Model
	Identifier string
	Email      string
	Hash       string
	Password   string
	DumpID     string
	Priority   int `gorm:"default:0"`
}

type DB struct {
	*gorm.DB
	insertChan *channels.InfiniteChannel
	errors     []error
}

func New(workers int) (*DB, error) {
	db, err := gorm.Open("postgres", "host=localhost port=5432 user=passwords dbname=passwords password=abc123!!! sslmode=disable")
	if err != nil {
		return nil, err
	}
	db.AutoMigrate(&Dump{})
	insertChan := channels.NewInfiniteChannel()
	d := &DB{db, insertChan, make([]error, 0)}

	for i := 0; i < workers; i++ {
		go d.insertWorker(insertChan.Out())
	}

	return d, nil
}

func (db *DB) insertWorker(insertChan <-chan interface{}) {
	for dumpI := range insertChan {
		dump, _ := dumpI.(Dump)
		if err := db.Create(&dump).Error; err != nil {
			db.errors = append(db.errors, err)
		}
	}
}

func (db *DB) increasePriority(ids []uint) error {
	return db.Model(Dump{}).Where("id IN (?)", ids).Update("priority", gorm.Expr("priority + 1")).Error
}

func (db *DB) GetHashes(identifier string) ([]string, error) {
	ids := make([]uint, 0)
	hashes := make([]string, 0)
	var raw []Dump

	result := db.Select("id, hash").Where("identifier = ?", identifier).Find(&raw)
	if result.Error != nil {
		return hashes, result.Error
	}

	for _, o := range raw {
		if o.Hash != "" {
			ids = append(ids, o.ID)
			hashes = append(hashes, o.Hash)
		}
	}

	if err := db.increasePriority(ids); err != nil {
		return hashes, err
	}

	return hashes, nil
}

func (db *DB) GetPasswords(identifier string) ([]string, error) {
	passwords := make([]string, 0)
	var raw []Dump
	result := db.Select("password").Where("identifier = ?", identifier).Find(&raw)
	if result.Error != nil {
		return passwords, result.Error
	}

	for _, o := range raw {
		if o.Password != "" {
			passwords = append(passwords, o.Password)
		}
	}
	return passwords, nil
}

func (db *DB) GetIdentifiers(password string) ([]string, error) {
	identifiers := make([]string, 0)
	var raw []Dump
	result := db.Select("identifier").Where("password = ?", password).Find(&raw)
	if result.Error != nil {
		return identifiers, result.Error
	}

	for _, o := range raw {
		identifiers = append(identifiers, o.Identifier)
	}
	return identifiers, nil
}

func (db *DB) Insert(val Dump) {
	db.insertChan.In() <- val
}

func (db *DB) Close() {
	db.Close()
}
