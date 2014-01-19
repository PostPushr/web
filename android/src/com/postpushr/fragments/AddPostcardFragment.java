package com.postpushr.fragments;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Fragment;
import android.content.Context;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.View.OnFocusChangeListener;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.postpushr.R;
import com.postpushr.fragments.HomeFragment.PostcardFlowListener;
import com.postpushr.fragments.SignInFragment.SignInListener;
import com.postpushr.model.Account;
import com.postpushr.model.Order;
import com.postpushr.model.Recipient;

public class AddPostcardFragment extends Fragment {

	private Bitmap mBitmap;
	// private ListAdapter mAdapter;
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

		/*
		 * ListView recipientsListView = (ListView)
		 * view.findViewById(R.id.addpostcard_recipients_listview); mAdapter =
		 * new RecipientsListAdapter(); recipientsListView.setAdapter(mAdapter);
		 */

		/*
		 * Button addRecipientButton = (Button)
		 * view.findViewById(R.id.addpostcard_addrecipient_button);
		 * addRecipientButton.setOnClickListener(new AddRecipientListener());
		 */
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

			EditText nameEdit = (EditText) view.findViewById(R.id.recipient_name_edittext);
			EditText addressEdit = (EditText) view.findViewById(R.id.recipient_address_edittext);
			EditText messageEdit = (EditText) view.findViewById(R.id.recipient_message_edittext);

			nameEdit.setOnFocusChangeListener(new OnFocusChangeListener() {
				@Override
				public void onFocusChange(View view, boolean hasFocus) {
					if (hasFocus)
						((EditText) view).selectAll();
				}
			});

			addressEdit.setOnFocusChangeListener(new OnFocusChangeListener() {
				@Override
				public void onFocusChange(View view, boolean hasFocus) {
					if (hasFocus)
						((EditText) view).selectAll();
				}
			});
			messageEdit.setOnFocusChangeListener(new OnFocusChangeListener() {
				@Override
				public void onFocusChange(View view, boolean hasFocus) {
					if (hasFocus)
						((EditText) view).selectAll();
				}
			});

			return view;
		}
	}

	/*
	 * private class AddRecipientListener implements OnClickListener {
	 * 
	 * @Override public void onClick(View arg0) { mNumRecipients++;
	 * ((BaseAdapter) mAdapter).notifyDataSetChanged(); }
	 * 
	 * }
	 */

	private class PostcardSendListener implements OnClickListener {
		@Override
		public void onClick(final View view) {

			try {
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
							HttpResponse txidResponse = httpclient.execute(httppost, localContext);

							BufferedReader reader = new BufferedReader(new InputStreamReader(txidResponse.getEntity().getContent(), "UTF-8"));
							StringBuilder builder = new StringBuilder();
							for (String line = null; (line = reader.readLine()) != null;) {
								builder.append(line).append("\n");
							}
							JSONObject txidObject = new JSONObject(builder.toString());
							String txid = txidObject.getString("txid");

							boolean waiting = true;
							boolean success = false;
							String errorCode = null;
							float price = 0f;
							String orderDate = null;
							do {
								HttpPost httppost2 = new HttpPost("http://postpushr.com/api/login");
								nameValuePairs = new ArrayList<NameValuePair>(1);
								nameValuePairs.add(new BasicNameValuePair("txid", txid));
								httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

								HttpResponse response2 = httpclient.execute(httppost2);

								BufferedReader reader2 = new BufferedReader(new InputStreamReader(response2.getEntity().getContent(), "UTF-8"));
								StringBuilder builder2 = new StringBuilder();
								for (String line = null; (line = reader2.readLine()) != null;) {
									builder2.append(line).append("\n");
								}
								JSONObject jsonObject2 = new JSONObject(builder2.toString());
								String statusCode = jsonObject2.getString("status");

								if (!(statusCode.equals("pending"))) {
									waiting = false;
									if (statusCode.equals("success")) {
										success = true;
										JSONObject successfulResults = jsonObject2.getJSONObject("results");
										price = (float) successfulResults.getDouble("price");
										orderDate = successfulResults.getString("date");
									} else if (statusCode.equals("error")) {
										success = false;
										errorCode = jsonObject2.getString("error");
									}
								}
							} while (waiting);
							if (!success) {
								Toast.makeText(getActivity(), "Error sending this postcard: " + errorCode, Toast.LENGTH_LONG).show();
							} else {
								Toast.makeText(getActivity(), "Success! You were charged $" + String.format("%.2d", price) + ".", Toast.LENGTH_LONG)
										.show();
								Account account = ((AccountHolder) getActivity()).getAccount();
								account.getOrders().add(new Order(orderDate, mBitmap, r, price));
								((SignInListener) getActivity()).moveToHomeFragment(account);
							}

						} catch (ClientProtocolException e) {
							// TODO Auto-generated catch block
						} catch (IOException e) {
							// TODO Auto-generated catch block
						} catch (JSONException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
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

	private class Edit extends EditText {
		public Edit(Context context) {
			super(context);
		}

		@Override
		public boolean onTouchEvent(MotionEvent e) {
			super.onTouchEvent(e);
			return false;
		}
	}
}