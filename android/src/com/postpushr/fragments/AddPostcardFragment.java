package com.postpushr.fragments;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;

import android.app.Fragment;
import android.content.Context;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.Toast;

import com.postpushr.R;
import com.postpushr.fragments.HomeFragment.PostcardFlowListener;
import com.postpushr.model.Account;
import com.postpushr.model.Recipient;

public class AddPostcardFragment extends Fragment {

	private String mName;
	private Bitmap mBitmap;
	private ListAdapter mAdapter;
	private int mNumRecipients;
	private String mPictureFilename;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		mNumRecipients = 1;
		super.onCreate(savedInstanceState);
		setHasOptionsMenu(true);
	}

	/*
	 * @Override public void onCreateOptionsMenu(Menu menu, MenuInflater
	 * inflater) {
	 * menu.findItem(R.id.home_actionbar_add_button).setVisible(false); }
	 */

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup parent, Bundle savedInstanceState) {
		View view = inflater.inflate(R.layout.fragment_addpostcard, parent, false);

		Button takePictureButton = (Button) view.findViewById(R.id.addpostcard_takepicture_button);
		takePictureButton.setOnClickListener(new TakePictureListener());

		ListView recipientsListView = (ListView) view.findViewById(R.id.addpostcard_recipients_listview);
		mAdapter = new RecipientsListAdapter();
		recipientsListView.setAdapter(mAdapter);

		Button addRecipientButton = (Button) view.findViewById(R.id.addpostcard_addrecipient_button);
		addRecipientButton.setOnClickListener(new AddRecipientListener());

		Button sendPostcardButton = (Button) view.findViewById(R.id.addpostcard_send_button);
		sendPostcardButton.setOnClickListener(new PostcardSendListener());

		return view;
	}

	private class TakePictureListener implements OnClickListener {

		@Override
		public void onClick(View arg0) {
			((PostcardFlowListener) getActivity()).executePostcardCameraIntent();
		}

	}

	public void setPictureFilename(Uri uri) {
		mPictureFilename = uri.getPath();
	}

	private class RecipientsListAdapter extends BaseAdapter {

		@Override
		public int getCount() {
			return mNumRecipients;
		}

		@Override
		public Object getItem(int position) {
			return position;
		}

		@Override
		public long getItemId(int position) {
			return position;
		}

		@Override
		public View getView(int position, View view, ViewGroup parent) {
			if (null == view) {
				LayoutInflater inflater = (LayoutInflater) getActivity().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
				view = inflater.inflate(R.layout.recipient_row, null);
			}
			return view;
		}

	}

	private class AddRecipientListener implements OnClickListener {

		@Override
		public void onClick(View arg0) {
			mNumRecipients++;
			((BaseAdapter) mAdapter).notifyDataSetChanged();
		}

	}

	private class PostcardSendListener implements OnClickListener {
		@Override
		public void onClick(final View view) {

			try {
				mName = ((EditText) getView().findViewById(R.id.addpostcard_name_edittext)).getText().toString();

				String nameBuf = null;
				String addressBuf = null;
				String messageBuf = null;

				Recipient[] recipients = new Recipient[mNumRecipients];

				try {
					for (int i = 0; i < mNumRecipients; i++) {
						nameBuf = ((EditText) getView().findViewById(R.id.recipient_name_edittext)).getText().toString();
						addressBuf = ((EditText) getView().findViewById(R.id.recipient_address_edittext)).getText().toString();
						messageBuf = ((EditText) getView().findViewById(R.id.recipient_message_edittext)).getText().toString();
						recipients[i] = new Recipient(nameBuf, addressBuf, messageBuf);
					}

					// check image

					for (Recipient r : recipients) {

						HttpClient httpclient = new DefaultHttpClient();
						HttpPost httppost = new HttpPost("http://postpushr.com/api/create/postcard");
						HttpContext localContext = new BasicHttpContext();
						List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(4);
						nameValuePairs.add(new BasicNameValuePair("username", ((AccountHolder) getActivity()).getAccount().getUsername()));
						nameValuePairs
								.add(new BasicNameValuePair("password", ((AccountHolder) getActivity()).getAccount().getHashedSaltedPassword()));
						nameValuePairs.add(new BasicNameValuePair("name", r.getName()));
						nameValuePairs.add(new BasicNameValuePair("address", r.getAddress()));
						nameValuePairs.add(new BasicNameValuePair("message", r.getMessage()));
						nameValuePairs.add(new BasicNameValuePair("picture", mPictureFilename));
						try {
							MultipartEntity entity = new MultipartEntity(HttpMultipartMode.BROWSER_COMPATIBLE);

							for (int index = 0; index < nameValuePairs.size(); index++) {
								if (nameValuePairs.get(index).getName().equalsIgnoreCase("picture")) {
									// If the key equals to "image", we use
									// FileBody to transfer the data
									entity.addPart(nameValuePairs.get(index).getName(), new FileBody(new File(nameValuePairs.get(index).getValue())));
								} else {
									// Normal string data
									entity.addPart(nameValuePairs.get(index).getName(), new StringBody(nameValuePairs.get(index).getValue()));
								}
							}

							httppost.setEntity(entity);

							httpclient.execute(httppost, localContext);

						} catch (ClientProtocolException e) {
							// TODO Auto-generated catch block
						} catch (IOException e) {
							// TODO Auto-generated catch block
						}

						// pop up dialog -"you've been charged"
					}

				} catch (NullPointerException e) {
					Toast.makeText(getActivity(), "Invalid recipient info, please enter valid information", Toast.LENGTH_LONG).show();
				}

			} catch (NullPointerException e) {
				Toast.makeText(getActivity(), "Invalid postcard name, please enter a name for this postcard", Toast.LENGTH_LONG).show();
			}

		}

	}

	public interface AccountHolder {

		public Account getAccount();

	}

}