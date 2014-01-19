package com.postpushr.model;

import java.text.DateFormat;

import android.annotation.SuppressLint;
import android.graphics.Bitmap;

public class Order {

	private final DateFormat mOrderDate;
	private final Bitmap mPicture;
	private final Recipient[] mRecipients;
	private final float mPrice;

	public Order(DateFormat orderDate, Bitmap picture, Recipient[] recipients,
			float price) {
		mOrderDate = orderDate;
		mPicture = picture;
		mRecipients = recipients;
		mPrice = price;
	}

	public String getOrderDateString() {
		// TODO test this formatting
		return DateFormat.getDateInstance(DateFormat.LONG).format(mOrderDate);
	}

	public Bitmap getPictureBitmap() {
		return mPicture;
	}

	public Recipient[] getRecipients() {
		return mRecipients;
	}

	@SuppressLint("DefaultLocale")
	public String getPriceString() {
		// TODO test this formatting
		return String.format("%.2f", mPrice);
	}

}
