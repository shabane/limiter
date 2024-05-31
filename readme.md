# Limiter

This Script will send you a telegram message whenever
your network usage reaches to a threshold that you specified.
this script will count and include **all your network** interfaces.


### Usage
    --limit LIMIT         Threshold Number Of Limit
    --chatid CHATID       Telegram User ChatId Or Channel @Username/ID
    --message MESSAGE     The Message As Notify[Optional]
    --token TOKEN         Telegram Bot Token
    --repeat-msg REPEAT_MSG Repeat Message Time[Miniut
    --send-startup-message  Send A Message That Indicate The Script Is Running

- Example
```bash
# Send Notify When Network Usage Rich 1TB

./limiter.py --limit 1_000_000 --chatid 1251603620  --token aaaaaa:bbbbbbbbb
```
