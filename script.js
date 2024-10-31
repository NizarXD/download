const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

// Koneksi ke MongoDB
mongoose.connect('mongodb://localhost:27017/bucinDB', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const LoveMessageSchema = new mongoose.Schema({
    message: String,
    userId: String,
});

const LoveMessage = mongoose.model('LoveMessage', LoveMessageSchema);

// Endpoint untuk mengirim pesan
app.post('/api/messages', async (req, res) => {
    const { message, userId } = req.body;
    const loveMessage = new LoveMessage({ message, userId });
    await loveMessage.save();
    res.json(loveMessage);
});

// Endpoint untuk mendapatkan pesan
app.get('/api/messages', async (req, res) => {
    const messages = await LoveMessage.find();
    res.json(messages);
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
