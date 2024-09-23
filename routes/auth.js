const express = require('express');
const bcrypt = require('bcryptjs');
const pool = require('../db');
const router = express.Router();

router.post('/register', async (req, res) => {
    const { firstname, lastname, email, username, password, phone, barangay, isadmin } = req.body;

    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser = await pool.query(
            `INSERT INTO users (firstname, lastname, email, username, password, phone, barangay, isadmin)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *`,
            [firstname, lastname, email, username, hashedPassword, phone, barangay, isadmin]
        );
        res.json(newUser.rows[0]);
    } catch (err) {
        console.error(err.message);
        res.status(500).json('Server error');
    }
});

module.exports = router;
