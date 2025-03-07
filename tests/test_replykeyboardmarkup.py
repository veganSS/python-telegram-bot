#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2022
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

import pytest

from telegram import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


@pytest.fixture(scope="class")
def reply_keyboard_markup():
    return ReplyKeyboardMarkup(
        TestReplyKeyboardMarkup.keyboard,
        resize_keyboard=TestReplyKeyboardMarkup.resize_keyboard,
        one_time_keyboard=TestReplyKeyboardMarkup.one_time_keyboard,
        selective=TestReplyKeyboardMarkup.selective,
    )


class TestReplyKeyboardMarkup:
    keyboard = [[KeyboardButton("button1"), KeyboardButton("button2")]]
    resize_keyboard = True
    one_time_keyboard = True
    selective = True

    def test_slot_behaviour(self, reply_keyboard_markup, mro_slots):
        inst = reply_keyboard_markup
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    @pytest.mark.flaky(3, 1)
    async def test_send_message_with_reply_keyboard_markup(
        self, bot, chat_id, reply_keyboard_markup
    ):
        message = await bot.send_message(chat_id, "Text", reply_markup=reply_keyboard_markup)

        assert message.text == "Text"

    @pytest.mark.flaky(3, 1)
    async def test_send_message_with_data_markup(self, bot, chat_id):
        message = await bot.send_message(
            chat_id, "text 2", reply_markup={"keyboard": [["1", "2"]]}
        )

        assert message.text == "text 2"

    def test_from_button(self):
        reply_keyboard_markup = ReplyKeyboardMarkup.from_button(
            KeyboardButton(text="button1")
        ).keyboard
        assert len(reply_keyboard_markup) == 1
        assert len(reply_keyboard_markup[0]) == 1

        reply_keyboard_markup = ReplyKeyboardMarkup.from_button("button1").keyboard
        assert len(reply_keyboard_markup) == 1
        assert len(reply_keyboard_markup[0]) == 1

    def test_from_row(self):
        reply_keyboard_markup = ReplyKeyboardMarkup.from_row(
            [KeyboardButton(text="button1"), KeyboardButton(text="button2")]
        ).keyboard
        assert len(reply_keyboard_markup) == 1
        assert len(reply_keyboard_markup[0]) == 2

        reply_keyboard_markup = ReplyKeyboardMarkup.from_row(["button1", "button2"]).keyboard
        assert len(reply_keyboard_markup) == 1
        assert len(reply_keyboard_markup[0]) == 2

    def test_from_column(self):
        reply_keyboard_markup = ReplyKeyboardMarkup.from_column(
            [KeyboardButton(text="button1"), KeyboardButton(text="button2")]
        ).keyboard
        assert len(reply_keyboard_markup) == 2
        assert len(reply_keyboard_markup[0]) == 1
        assert len(reply_keyboard_markup[1]) == 1

        reply_keyboard_markup = ReplyKeyboardMarkup.from_column(["button1", "button2"]).keyboard
        assert len(reply_keyboard_markup) == 2
        assert len(reply_keyboard_markup[0]) == 1
        assert len(reply_keyboard_markup[1]) == 1

    def test_expected_values(self, reply_keyboard_markup):
        assert isinstance(reply_keyboard_markup.keyboard, list)
        assert isinstance(reply_keyboard_markup.keyboard[0][0], KeyboardButton)
        assert isinstance(reply_keyboard_markup.keyboard[0][1], KeyboardButton)
        assert reply_keyboard_markup.resize_keyboard == self.resize_keyboard
        assert reply_keyboard_markup.one_time_keyboard == self.one_time_keyboard
        assert reply_keyboard_markup.selective == self.selective

    def test_wrong_keyboard_inputs(self):
        with pytest.raises(ValueError):
            ReplyKeyboardMarkup([["button1"], "Button2"])
        with pytest.raises(ValueError):
            ReplyKeyboardMarkup("button")

    def test_to_dict(self, reply_keyboard_markup):
        reply_keyboard_markup_dict = reply_keyboard_markup.to_dict()

        assert isinstance(reply_keyboard_markup_dict, dict)
        assert (
            reply_keyboard_markup_dict["keyboard"][0][0]
            == reply_keyboard_markup.keyboard[0][0].to_dict()
        )
        assert (
            reply_keyboard_markup_dict["keyboard"][0][1]
            == reply_keyboard_markup.keyboard[0][1].to_dict()
        )
        assert (
            reply_keyboard_markup_dict["resize_keyboard"] == reply_keyboard_markup.resize_keyboard
        )
        assert (
            reply_keyboard_markup_dict["one_time_keyboard"]
            == reply_keyboard_markup.one_time_keyboard
        )
        assert reply_keyboard_markup_dict["selective"] == reply_keyboard_markup.selective

    def test_equality(self):
        a = ReplyKeyboardMarkup.from_column(["button1", "button2", "button3"])
        b = ReplyKeyboardMarkup.from_column(
            [KeyboardButton(text) for text in ["button1", "button2", "button3"]]
        )
        c = ReplyKeyboardMarkup.from_column(["button1", "button2"])
        d = ReplyKeyboardMarkup.from_column(["button1", "button2", "button3.1"])
        e = ReplyKeyboardMarkup([["button1", "button1"], ["button2"], ["button3.1"]])
        f = InlineKeyboardMarkup.from_column(["button1", "button2", "button3"])

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)

        assert a != f
        assert hash(a) != hash(f)
