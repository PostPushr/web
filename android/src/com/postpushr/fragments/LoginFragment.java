package com.postpushr.fragments;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Fragment;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.postpushr.R;
import com.postpushr.Util;
import com.postpushr.fragments.SignInFragment.SignInListener;
import com.postpushr.model.Account;
import com.postpushr.model.Order;
import com.postpushr.model.Recipient;

public class LoginFragment extends Fragment {

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		getActivity().setTitle("Login");
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup parent, Bundle savedInstanceState) {
		View view = inflater.inflate(R.layout.fragment_login, parent, false);
		Button loginSubmitButton = (Button) view.findViewById(R.id.login_submit_button);
		loginSubmitButton.setOnClickListener(new LoginSubmitListener());
		return view;
	}

	private class LoginSubmitListener implements OnClickListener {
		@Override
		public void onClick(View view) {

			final String username = ((EditText) getView().findViewById(R.id.login_email_edittext)).getText().toString();
			final String password = ((EditText) getView().findViewById(R.id.login_password_edittext)).getText().toString();
			System.out.println("DEBUGG:" + username + ":" + password);
			final String hashedSaltedPassword = Util.hashAndSaltPassword(password);
			try {
				// TODO: validate the info with the server
				HttpClient httpclient = new DefaultHttpClient();
				HttpPost httppost = new HttpPost("http://postpushr.com/api/login");
				List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
				nameValuePairs.add(new BasicNameValuePair("username", username));
				nameValuePairs.add(new BasicNameValuePair("password", hashedSaltedPassword));
				httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

				HttpResponse response = httpclient.execute(httppost);

				BufferedReader reader = new BufferedReader(new InputStreamReader(response.getEntity().getContent(), "UTF-8"));
				StringBuilder builder = new StringBuilder();
				for (String line = null; (line = reader.readLine()) != null;) {
					builder.append(line).append("\n");
				}
				JSONObject jsonObject = new JSONObject(builder.toString());

				if (jsonObject.get("status").equals("success")) {
					JSONArray resultsArray = jsonObject.getJSONArray("results");
					List<Order> orders = new ArrayList<Order>();
					for (int i = 0; i < resultsArray.length(); i++) {
						JSONObject orderObject = resultsArray.getJSONObject(i);

						Bitmap bm = null;
						try {
							URL aURL = new URL(orderObject.getString("picture"));
							URLConnection conn = aURL.openConnection();
							conn.connect();
							InputStream is = conn.getInputStream();
							BufferedInputStream bis = new BufferedInputStream(is);
							bm = BitmapFactory.decodeStream(bis);
							bis.close();
							is.close();
						} catch (IOException e) {
							Log.e("LoginFragment", "Error getting bitmap", e);
						}

						orders.add(new Order(orderObject.getString("date"), bm, new Recipient(orderObject.getString("name"), orderObject
								.getString("address"), orderObject.getString("message")), (float) orderObject.getDouble("price")));
					}
					((SignInListener) getActivity()).moveToHomeFragment(new Account(username, hashedSaltedPassword, orders));
				} else {
					Toast.makeText(getActivity(), "Login failed. Check your login info and try again.", Toast.LENGTH_LONG).show();
				}

			} catch (ClientProtocolException e) {
				// TODO Auto-generated catch block
			} catch (IOException e) {
				// TODO Auto-generated catch block
			} catch (JSONException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			// Assuming success, and getting the list of orders
			((SignInListener) getActivity()).moveToHomeFragment(new Account(username, hashedSaltedPassword, null));
		}
	}
}
